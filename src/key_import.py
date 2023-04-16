import database
import msgpack
import logging
from env import Env
from os import environ
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

if Env.get_mongo_srv() is None:
    logging.fatal('connection string not found!')

key_path = input('Enter key path:')

with database.Database() as db:

    key = None
    with open(key_path, 'rb') as file:
        key = file.read()

    key = msgpack.unpackb(key)

    db.add_client(key)

    logging.info("key imported successfully")

logging.info("done")