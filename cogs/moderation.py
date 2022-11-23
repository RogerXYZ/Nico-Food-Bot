from doctest import debug_script
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from helpers import db_manager


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.
        """
        embed = discord.Embed(
            description="baj baj <:ZULUL:1044752565897797692> 👋",
            color=0x161568
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @checks.is_owner()
    async def say(self, context: Context, message: str) -> None:
        """
        The bot will say anything you want.
        """
        await context.send("<:forsenE:1044752862825156669> : " + message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @checks.is_owner()
    async def embed(self, context: Context, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.
        """
        embed = discord.Embed(
            description="<:forsenE:1044752862825156669> : " + message,
            color=0x161568
        )
        await context.send(embed=embed)

    @commands.hybrid_group(
        name="blacklist",
        description="Get the list of all blacklisted users.",
    )
    @checks.is_owner()
    async def blacklist(self, context: Context) -> None:
        """
        Lets you add or remove a user from not being able to use the bot.
        """
        pass

    @blacklist.command(
        base="blacklist",
        name="add",
        description="Lets you add a user from not being able to use the bot.",
    )
    @checks.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        """
        Lets you add a user from not being able to use the bot.
        """
        user_id = user.id
        if db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is not in the blacklist.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        total = db_manager.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            title="User Blacklisted",
            description=f"**{user.name}** has been successfully added to the blacklist",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)

    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Lets you remove a user from not being able to use the bot.",
    )
    @checks.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User):
        """
        Lets you remove a user from not being able to use the bot.
        """
        user_id = user.id
        if not db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                title="Error!",
                description=f"**{user.name}** is already in the blacklist.",
                color=0xE02B2B
            )
            return await context.send(embed=embed)
        total = db_manager.remove_user_from_blacklist(user_id)
        embed = discord.Embed(
            title="User removed from blacklist",
            description=f"**{user.name}** has been successfully removed from the blacklist",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"There are now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
