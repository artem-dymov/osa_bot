import requests
import json
from utils.db_api.models import faculties_ukr, faculties
from utils.db_api import db_commands
import asyncio
from utils.db_api.database import create_db, drop_connection
from utils.db_api import models

