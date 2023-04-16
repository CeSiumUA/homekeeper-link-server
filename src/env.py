from os import environ

class Env:
    MONGO_SRV = 'MONGO_SRV'
    MONGO_DB = 'MONGO_DB'
    PORT = 'PORT'
    ADDRESS = 'ADDRESS'

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