import os
from os.path import join, dirname

from dotenv import load_dotenv

# load .env file and vars
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# bot settings
prefix = "!"
description = "OHSEA Verification Bot"

# ID's
verified_role_id = 845223569034182726

