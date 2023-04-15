import database
import server
import os
import processor
from dotenv import load_dotenv

load_dotenv()

address = os.environ("HOMEKEEPER_ADDRESS")
port = os.environ("HOMEKEEPER_PORT")

with database.Database() as db:

    db.ensure_index_created()

    cp = processor.Processor(db)

    with server.Server(address=address, port=port, cp=cp) as srv:
        input("Type anything to exit...")

print("Server closed")