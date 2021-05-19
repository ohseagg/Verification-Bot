import discord
from discord.ext import commands

from settings import BOT_TOKEN, prefix, description

# discord gateway intents
intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False,
                                           users=True,
                                           roles=False)

# bot instance
bot = discord.ext.commands.Bot(command_prefix=prefix,
                               intents=intents,
                               description=description,
                               case_insensitive=True,
                               allowed_mentions=allowed_mentions)


@bot.command()
async def placeholder(ctx):
    await ctx.send('Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
                   'sed do eiusmod tempor incididunt ut labore et dolore '
                   'magna aliqua. Ut enim ad minim veniam, quis nostrud '
                   'exercitation ullamco laboris nisi ut aliquip ex ea '
                   'commodo consequat. Duis aute irure dolor in '
                   'reprehenderit in voluptate velit esse cillum dolore eu '
                   'fugiat nulla pariatur. Excepteur sint occaecat cupidatat '
                   'non proident, sunt in culpa qui officia deserunt mollit '
                   'anim id est laborum.')


# run the bot
# INVITE LINK: https://discord.com/api/oauth2/authorize?client_id=844487751835451412&permissions=470150256&scope=bot
bot.run(BOT_TOKEN)
