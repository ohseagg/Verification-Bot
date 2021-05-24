import pytz
from datetime import datetime
from settings import daylight_savings

import discord


async def timestamp_string():
    est = pytz.timezone('US/Eastern')
    fmt = '%Y-%m-%d %I:%M:%S %p %Z'

    winter = datetime.now()
    summer = datetime.now()

    if daylight_savings:
        return summer.astimezone(est).strftime(fmt)
    else:
        return winter.astimezone(est).strftime(fmt)


async def error_embed(message: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.red())
    # set title field
    embed.add_field(name=f"Error!", value=message)

    # return finished embed
    return embed


async def success_embed(message: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.green())
    # set title field
    embed.add_field(name=f"Success!", value=message)

    # return finished embed
    return embed


async def registration_embed(user: dict, user_id: int):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.gold())
    # set title field
    embed.add_field(name=f"User Registered",
                    value=f"<@{user_id}> just registered.",
                    inline=False)

    # add name fields
    embed.add_field(name=f"First Name",
                    value=user['first_name'],
                    inline=True)
    embed.add_field(name=f"Last Name",
                    value=user['last_name'],
                    inline=True)
    embed.add_field(name=f"Email",
                    value=user['email'],
                    inline=True)

    embed.set_footer(text=await timestamp_string(),
                     icon_url="https://image.brandonly.me/ohsea/WhiteOnNavy.png")

    # return finished embed
    return embed


async def verification_embed(user_id: int, nick: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.green())
    # set title field
    embed.add_field(name=f"User Verified",
                    value=f"<@{user_id}> ({nick}) just verified.")

    embed.set_footer(text=await timestamp_string(),
                     icon_url="https://image.brandonly.me/ohsea/WhiteOnNavy.png")

    # return finished embed
    return embed

