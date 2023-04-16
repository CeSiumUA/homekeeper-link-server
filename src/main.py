import database
import server
import os
import processor
import logging
from env import Env
from dotenv import load_dotenv

load_dotenv()

address = Env.get_address()
port = Env.get_port()

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

with database.Database() as db:

    db.ensure_index_created()

    cp = processor.Processor(db)

    with server.Server(address=address, port=port, cp=cp) as srv:
        input("Type anything to exit...")

logging.info("Server closed")