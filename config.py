class Config:
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tarefas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20 # Aumenta o pool para conexões simultâneas
    SQLALCHEMY_POOL_RECYCLE = 280 # Recicla conexões para evitar timeouts
    JWT_SECRET_KEY = 'jwt-secret-key'
