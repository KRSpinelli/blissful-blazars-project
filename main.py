"""
Cog Loading Service. THIS CODE MUST BE RAN FIRST
"""
import os
import sys

import interactions
from dotenv import load_dotenv

from config import DEBUG, DEV_GUILD, TOKEN
from src import logutil

load_dotenv()

# Configure logging for this main.py handler
logger = logutil.init_logger("main.py")
logger.debug(
    "Debug mode is %s; This is not a warning, \
just an indicator. You may safely ignore",
    DEBUG,
)


if not TOKEN:
    logger.critical("TOKEN variable not set. Cannot continue")
    sys.exit(1)

client = interactions.Client(
    token=TOKEN,
    send_not_ready_messages=True,
    activity=interactions.Activity(
        name="Credibility Connoisseur", type=interactions.ActivityType.PLAYING
    ),
    debug_scope=DEV_GUILD,
)


@interactions.listen()
async def on_startup():
    """Called when the bot starts"""
    logger.info(f"Logged in as {client.user}")


# get all python files in "extensions" folder
extensions = [
    f"extensions.{f[:-3]}"
    for f in os.listdir("./extensions")
    if f.endswith(".py") and not f.startswith("_")
]
for extension in extensions:
    try:
        client.load_extension(extension)
        logger.info(f"Loaded extension {extension}")
    except interactions.errors.ExtensionLoadException as e:
        logger.exception(f"Failed to load extension {extension}.", exc_info=e)

client.sync_interactions = True

client.start()