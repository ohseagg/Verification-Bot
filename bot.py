from string import capwords

import discord


from discord.ext.commands import Context, Bot
from embeds import error_embed, success_embed
from settings import BOT_TOKEN, prefix, description, verified_role_id
from settings import verification_channel_id
from database import emailTaken, addVerification, verifyUser, idTaken
from database import isEDUEmail, addEDUEmail, authCodeTaken
from mailgun import email_auth_code

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
                                               'EDU email!'
                                               '\n\n'
                                               'Contact modmail if you\'d'
                                               'like to add yours.'))

    # check if email is already used
    if await emailTaken(msg.content):
        await ctx.send(embed=await error_embed('Your email is already taken!'
                                               '\n\nPlease contact modmail'
                                               'if you think this '
                                               'was a mistake.'))
    # otherwise add user to verification
    else:
        await addVerification(user)
        await ctx.send(embed=await success_embed('Check your email for further'
                                                 ' instructions :smile:'))


@bot.command()
async def verify(ctx: discord.ext.commands.Context, auth_code=None):
    # check if auth code was provided
    if auth_code is None:
        await ctx.send(embed=await error_embed("No email verification code "
                                               "provided."))
        # cancel the command
        return

    # command can only be run verification channel
    elif ctx.channel.id != verification_channel_id:
        await ctx.send(embed=await error_embed(f"Command can only be run in "
                                               f"<#{verification_channel_id}>"))
        return

    # check if user is already verified
    elif await idTaken(ctx.author.id):
        await ctx.send(embed=await error_embed("Your ID is already registered."
                                               "\n"
                                               "If you think this was a "
                                               "mistake "
                                               "please contact an admin."))
        return

    # check if auth code is valid
    elif not await authCodeTaken(auth_code):
        await ctx.reply(embed=await error_embed("Not a valid verification "
                                                "code."))
        return

    # verify user
    nick = await verifyUser(ctx.author.id, auth_code)
    await ctx.reply(embed=await success_embed("You're in! :smile:"))
    # give role
    await ctx.author.add_roles(ctx.guild.get_role(verified_role_id))
    await ctx.author.edit(nick=nick)


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
bot.run(BOT_TOKEN)
