from settings import verification_log_channel_id
from embeds import registration_embed, verification_embed


async def logRegistered(ctx, user, bot):
    log_channel = bot.get_channel(verification_log_channel_id)
    await log_channel.send(embed=await registration_embed(user, ctx.author.id))


async def logVerified(ctx, nick, bot):
    log_channel = bot.get_channel(verification_log_channel_id)
    await log_channel.send(embed=await verification_embed(ctx.author.id, nick))
