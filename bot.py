from string import capwords

import discord
import requests
import json

from discord.ext import commands
from embeds import error_embed, success_embed
from settings import BOT_TOKEN, prefix, description, verified_role_id
from settings import verification_channel_id
from database import emailTaken, addVerification, verify
from database import isEDUEmail, addEDUEmail

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
async def register(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=await error_embed("Command can only be run "
                                               "in my DM's!"))
        return

    def messageCheck(message):
        return message.channel == ctx.channel and ctx.author == message.author

    user = {}

    # get first name
    await ctx.send('What is your first name?')
    msg = await bot.wait_for('message',
                             check=messageCheck,
                             timeout=1800)
    user['first_name'] = capwords(msg.content)

    # get last name
    await ctx.send('What is your last name?')
    msg = await bot.wait_for('message',
                             check=messageCheck,
                             timeout=1800)
    user['last_name'] = capwords(msg.content)

    while True:
        # get email
        await ctx.send('What is your school email?')
        msg = await bot.wait_for('message',
                                 check=messageCheck,
                                 timeout=1800)
        user['email'] = msg.content

        # break out if valid edu email
        if await isEDUEmail(msg.content):
            break

        # else tell them its not a valid edu email
        await ctx.send(embed=await error_embed('That is not a valid '
                                               'EDU email!'))

    # check if email is already used
    if await emailTaken(msg.content):
        await ctx.send(embed=await error_embed('Your email is already taken!'
                                               '\n\nPlease contact an admin'
                                               'if you think this '
                                               'was a mistake.'))
    # otherwise add user to verification
    else:
        await addVerification(user)
        await ctx.send(embed=await success_embed('Check your email for further'
                                                 ' instructions :smile:'))


@bot.command()
async def verify(ctx, auth_code=None):
    # command can only be run verification channel
    if ctx.channel.id != verification_channel_id:
        await ctx.send(embed=await error_embed(f"Command can only be run in "
                                               f"<#{verification_channel_id}>"))
        return

    # check if auth code was provided
    if auth_code is None:
        await ctx.send(embed=await error_embed("No email verification code "
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

    # if 403 from id already taken
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


@bot.command()
async def addemail(ctx, address):
    if await isEDUEmail(address, True):
        await ctx.send(embed=await error_embed('Already a valid '
                                               'email address.'))
    else:
        await addEDUEmail(address)
        await ctx.send(embed=await success_embed(f'Added @{address} as a '
                                                 f'valid email address.'))

# run the bot
# INVITE LINK: https://discord.com/api/oauth2/authorize?client_id=844487751835451412&permissions=470150256&scope=bot
bot.run(BOT_TOKEN)
