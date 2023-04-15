import server

address = "0.0.0.0"
port = 25534

with server.Server(address=address, port=port) as srv:
    input("Type anything to exit...")

print("Server closed")