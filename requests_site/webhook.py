from datetime import datetime

import discord
from discord import RequestsWebhookAdapter, Webhook
from flask import current_app

from requests_site.decorator import run_async

colors = {
    0: discord.Colour(0xE29519),
    1: discord.Colour(0xA82033),
}


@run_async
def send_hook_async(url, event_type, embed):
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    webhook.send(f"New event: {event_type}", embed=embed)


def send_hook(event_type, beatmap):
    app = current_app._get_current_object()
    if "DISCORD_WEBHOOKS" not in app.config:
        return
    hooks = app.config["DISCORD_WEBHOOKS"]
    if not hooks:
        return

    for condition, url in hooks.items():
        try:
            result = eval(condition, {"req": beatmap})
        except:
            continue

        if not result:
            continue

        desc = (
            f"URL: {beatmap.link}\r\n"
            + f"Mapper: {beatmap.mapper}\r\n"
            + f"Requester: {beatmap.requester.username}\r\n"
            + f"Status: {beatmap.status.name}\r\n"
            + f"Target BN: {beatmap.target_bn.username}"
        )

        embed = discord.Embed(
            title=f"{beatmap.song}",
            colour=colors.get(beatmap.status_, discord.Colour(0x4A90E2)),
            description=desc,
            timestamp=datetime.utcnow(),
        )

        send_hook_async(url, event_type, embed)
