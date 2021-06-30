from datetime import datetime

import discord


async def error_embed(message: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.red())
    # set title field
    embed.add_field(name=f"Error!", value=message)

    # return finished embed
    return embed


async def success_embed(message: str):
    # generate embed with green colour
    embed = discord.Embed(color=discord.Colour.green())
    # set title field
    embed.add_field(name=f"Success!", value=message)

    # return finished embed
    return embed


async def registration_embed(user: dict, user_id: int):
    # generate embed with gold colour
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

    embed.timestamp = datetime.now()

    embed.set_footer(text=f"ID: {user_id}",
                     icon_url="https://image.brandonly.me/ohsea/WhiteOnNavy.png")

    # return finished embed
    return embed


async def verification_embed(user_id: int, nick: str):
    # generate embed with green colour
    embed = discord.Embed(color=discord.Colour.green())
    # set title field
    embed.add_field(name=f"User Verified",
                    value=f"<@{user_id}> ({nick}) just verified.")

    embed.timestamp = datetime.now()

    embed.set_footer(text=f"ID: {user_id}",
                     icon_url="https://image.brandonly.me/ohsea/WhiteOnNavy.png")

    # return finished embed
    return embed


async def rejoin_embed(user_id: int, nick: str):
    # generate embed with blue colour
    embed = discord.Embed(color=discord.Colour.blue())
    # set title field
    embed.add_field(name=f"User Rejoined",
                    value=f"<@{user_id}> ({nick}) just rejoined the server.")

    embed.timestamp = datetime.now()

    embed.set_footer(text=f"ID: {user_id}",
                     icon_url="https://image.brandonly.me/ohsea/WhiteOnNavy.png")

    # return finished embed
    return embed


async def infoCheckEmbed(user: dict, user_id: int):
    # generate embed with gold colour
    embed = discord.Embed(color=discord.Colour.gold())
    # set title field
    embed.add_field(name=f"Is this info correct?",
                    value=f"Please double check your information.",
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

    embed.timestamp = datetime.now()

    embed.set_footer(text=f"ID: {user_id}",
                     icon_url="https://image.brandonly.me/ohsea/WhiteOnNavy.png")

    # return finished embed
    return embed

