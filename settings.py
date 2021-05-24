import os
from os.path import join, dirname

from dotenv import load_dotenv

# load .env file and vars
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# database setttings
DBuser = os.getenv('DBuser')
DBpass = os.getenv('DBpass')
DBurl = os.getenv('DBurl')

# bot settings
prefix = "!"
description = "OHSEA Verification Bot"

# ID's
verified_role_id = 845223569034182726
verification_channel_id = 846190415980134430
