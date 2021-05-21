import discord


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
