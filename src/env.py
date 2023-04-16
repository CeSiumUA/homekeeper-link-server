from os import environ

class Env:
    MONGO_SRV = 'MONGO_SRV'
    MONGO_DB = 'MONGO_DB'
    PORT = 'PORT'
    ADDRESS = 'ADDRESS'
    NOTIFY_INTERVAL = 'NOTIFY_INTERVAL'
    CHAT_ID = 'CHAT_ID'
    TL_TOKEN = 'TL_TOKEN'

    def get_mongo_srv():
        return environ.get(Env.MONGO_SRV)
    
    def get_mongo_db():
        return environ.get(Env.MONGO_DB)
    
    def get_port():
        port = environ.get(Env.PORT)
        if port is None:
            return port
        
        return int(port)
    
    def get_address():
        return environ.get(Env.ADDRESS)
    
    def get_notify_interval_ns():
        return Env.get_notify_interval() * 10e9
    
    def get_notify_interval():
        interval = environ.get(Env.NOTIFY_INTERVAL)

        if interval is None:
            interval = 120

        return int(interval)
    
    def get_chat_id():
        id = environ.get(Env.CHAT_ID)
        if id is None:
            return id
        return int(id)
    
    def get_tl_token():
        return environ.get(Env.TL_TOKEN)