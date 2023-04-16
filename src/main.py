import database
import server
import os
import processor
from env import Env
from dotenv import load_dotenv

load_dotenv()

address = Env.get_address()
port = Env.get_port()

with database.Database() as db:

    db.ensure_index_created()

    cp = processor.Processor(db)

    with server.Server(address=address, port=port, cp=cp) as srv:
        input("Type anything to exit...")

print("Server closed")