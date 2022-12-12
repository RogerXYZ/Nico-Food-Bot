""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.0
"""
import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
    
    #Nico Food
    @commands.hybrid_command(
    name = "nico-food",
    description = "nico food"
    )
    async def forsen(self, context: Context):
        with open("nicofood.txt", "r") as foods:
            nicofoodlist = foods.readlines()
            nicofoo = nicofoodlist[random.randint(0,(len(nicofoodlist)-1))]
            await context.send(nicofoo)
    
    #Nico Food Add
    @commands.hybrid_command(
    name = "nico-food-add",
    description = "add nico food"
    )
    async def forsennn(self, context: Context, food_nico: str = None):
        with open("nicofood.txt", "a") as foods:
            foods.write(f"\n{food_nico}")
        await context.send("nico food added")


    #Literally Me
    @commands.hybrid_group(
        name = "literally-me",
        description = "He is litteraly me..."
    )
    async def goscat(self, context: Context) -> None:
        """
        He is litteraly me though
        """
        pass

    #Literally Me Random
    @goscat.command(
    base = "literally-me",
    name = "random",
    description = "He is literally me..."
    )
    async def forsen(self, context: Context):
        with open("gosling.txt", "r") as gosc:
            ryangosl = gosc.readlines()
            gosli = ryangosl[random.randint(0,(len(ryangosl)-1))]
            await context.send(gosli)
    
    #Literally Me Add
    @goscat.command(
    base = "literally-me",
    name = "add",
    description = "He is literally me..."
    )
    async def forsennn(self, context: Context, ryan_gosling: str = None):
        with open("gosling.txt", "a") as gosc:
            gosc.write(f"\n{ryan_gosling}")
        await context.send("Literally Me Added <:gosling:1044809002644676768>")


    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.
        
        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0xA61818
        )
        if context.guild.icon is not None:            
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms. <:amongE:1044765339583520838>",
            color=0xA61818
        )
        await context.send(embed=embed)



async def setup(bot):
    await bot.add_cog(General(bot))
