"""
code for jarvis defence system to notify israeli users from threats
"""
from textwrap import dedent
import io
import datetime
import discord
from discord.ext import tasks
from dotenv import dotenv_values
from maps import combine_images

PROFILER = False
DEBUG = True

if DEBUG:
    from red_alert_test import RedAlert
else:
    from red_alert import RedAlert

if PROFILER:
    import cProfile
    import pstats
    profiler = cProfile.Profile()
    profiler.enable()

alerts = RedAlert()
secrets = dotenv_values(".env")
TOKEN = secrets["DISCORD_KEY"]
intents = discord.Intents.all()
client = discord.Client(intents=intents)
last_alert = 0

@client.event
async def on_ready():
    """when the bot is ready, set the tree for commands and start the loops"""
    alert.start()
    await msg_to_id(1106198666047406170, "process started!")

async def msg_to_id(channel_id, message):
    """sends a message to a given channel id"""
    channel = client.get_channel(channel_id)
    num = 2000
    for index in range(0, len(message), num):
        await channel.send(content=message[index: index + num])

async def img_msg_to_id(channel_id, image, message, reference=None):
    """sends a message to a given channel id"""
    channel = client.get_channel(channel_id)
    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await channel.send(
            content=message, 
            file=discord.File(fp=image_binary, filename='map.png'),
            reference=reference
            )


async def alert_msg(channel_id, category, message):
    """sends a special alert message to a given channel id"""
    channel = client.get_channel(channel_id)
    embed = discord.Embed(
        title=f"**{category.upper()}**",
        description=message,
        color=discord.Color.red()
    )
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_author(name="JARVIS DEFENCE SYSTEM RED ALERT", icon_url="https://cdn-icons-png.flaticon.com/512/559/559343.png")
    return await channel.send(embed=embed)

@tasks.loop(seconds=1)
async def alert():
    """missile alert system in israel"""
    global last_alert
    global secrets
    red_alerts = alerts.get_red_alerts()
    if red_alerts is None:
        return None
    if last_alert == red_alerts["id"]:
        return None
    last_alert = red_alerts["id"]
    msg = dedent(f"""
        **{', '.join(red_alerts['english_cities'])}!
        {red_alerts['desc']}**
        this system was built with :heart: by Tomer
        """)
    if "חיפה - כרמל ועיר תחתית" in red_alerts["data"]:
        channel_id = int(secrets["SPECIFIC_ALERT"])
    else:
        channel_id = int(secrets["ALL_ALERTS"])
    reference = await alert_msg(
        channel_id,
        red_alerts["title"],
        f"<@307851424891404288>{msg}"
        )
    img = combine_images(red_alerts)
    await img_msg_to_id(
        channel_id,
        img,
        "here is a map of the affected areas:",
        reference=reference
        )
    if PROFILER:
        profiler.disable()
        profiler.print_stats(sort='cumulative')
        profiler_output = "profile_stats.txt"
        profiler.dump_stats(profiler_output)
        stats = pstats.Stats(profiler_output)
        stats.strip_dirs().sort_stats('cumulative').print_stats()
client.run(TOKEN)