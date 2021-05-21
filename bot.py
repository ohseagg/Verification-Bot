import discord
import requests
import json

from discord.ext import commands
from embeds import error_embed, success_embed
from settings import BOT_TOKEN, prefix, description, verified_role_id

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
async def verify(ctx, auth_code=None):
    # check if auth code was provided
    if auth_code is None:
        await ctx.reply(embed=await error_embed("No email verification code "
                                                "provided."))
        # cancel the command
        return

    url = "http://api.ohsea.gg:8080/verify"
    payload = json.dumps({
        "id": ctx.author.id,
        "auth_code": auth_code
    })

    # make request
    response = requests.post(url, data=payload)

    # if 403 from id already t aken
    if response.status_code == 403:
        await ctx.reply(embed=await error_embed("Your account has already "
                                                "been verified."))
    # send error message only if a 400 error
    elif response.status_code != 200:
        await ctx.reply(embed=await error_embed("Not a valid verification "
                                                "code."))
    # let in otherwise
    else:
        # response
        await ctx.reply(embed=await success_embed("You're in! :smile:"))
        # give role
        await ctx.author.add_roles(ctx.guild.get_role(verified_role_id))

# run the bot
# INVITE LINK: https://discord.com/api/oauth2/authorize?client_id=844487751835451412&permissions=470150256&scope=bot
bot.run(BOT_TOKEN)
