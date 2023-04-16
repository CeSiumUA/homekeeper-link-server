import database
import msgpack
from env import Env
from os import environ
from dotenv import load_dotenv

load_dotenv()

if Env.get_mongo_srv() is None:
    print('connection string not found!')
    exit(1)

key_path = input('Enter key path:')

with database.Database() as db:

    key = None
    with open(key_path, 'rb') as file:
        key = file.read()

    key = msgpack.unpackb(key)

    db.add_client(key)

    print("key imported successfully")

print("done")