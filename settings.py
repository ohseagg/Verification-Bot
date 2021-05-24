import os
from os.path import join, dirname

from dotenv import load_dotenv

if not os.getenv('dev') == 'True':
    # load .env file and vars if in dev mode
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')

# mailgun settings
mailgun_API_key = os.getenv('mailgun_API_key')
mailgun_base_URL = os.getenv('mailgun_base_URL')

# database settings
DBuser = os.getenv('DBuser')
DBpass = os.getenv('DBpass')
DBurl = os.getenv('DBurl')

# bot settings
prefix = "!"
description = "OHSEA Verification Bot"

# ID's
guild_id = 822264218492862504
verified_role_id = 846223942943506452
verification_channel_id = 846209783290658826
verification_log_channel_id = 846467953469685801

# timezone for timestamp
daylight_savings = True
