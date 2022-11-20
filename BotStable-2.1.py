import os
import unicodedata
import random
import asyncio
import json
import os
import platform
import random
import sqlite3
import sys
from contextlib import closing

import discord
from discord import Interaction
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

import exceptions

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents, help_command=None, token = TOKEN)

def init_db():
    with closing(connect_db()) as db:
        with open("database/schema.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect("database/database.db")

bot.config = config
bot.db = connect_db()


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()
    await bot.tree.sync()

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot
    """
    statuses = ["forsen", "forsen", "forsen"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return

    """
    Logging
    """
    messageL = f"{message.author}: {message.content} | {message.channel}/{message.guild}" 
    print(messageL)
    with open("genlogs.txt", "a", encoding="utf-8") as forsenf:
        unicodedata.normalize("NFC", messageL).encode("ascii", "ignore")
        forsenf.write("\n"+messageL)

    """
    forsen
    """
    forss = message.content.lower().find("forsen")
    if forss == -1:
        None
    elif message.author == "R0g3rXY#5994" and random.randint(0,10) == 4:
        await message.channel.send("forsen")
    elif random.randint(0,1000) == 420:
        await message.channel.send("forsen")

    """
    W or L
    """
    good_response = ["w bot", "good bot", "great bot", "nice bot"]
    bad_response = ["l bot", "bad bot", "horrible bot", "shit bot"]
    for item in good_response:
        itemfind = message.content.lower().find(item)
        if itemfind == -1:
            continue
        else:
            await message.channel.send(":3")
            break
    for item in bad_response:
        itemfind = message.content.lower().find(item)
        if itemfind == -1:
            continue
        else:
            await message.channel.send(":(")
            break  
    await bot.process_commands(message)


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        print(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.not_blacklisted() check in your command, or you can raise the error by yourself.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        """
        Same as above, just for the @checks.is_owner() check.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are not the owner of the bot!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

init_db()
asyncio.run(load_cogs())
bot.run(TOKEN)