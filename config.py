import os

application_absolute_dir = os.path.abspath(os.path.dirname((__file__)))

class Config:
    # Acess config
    SECRET_KEY = os.environ.get('G6Rf5Q3npCsgMHgq') or'you-will-never-guess.'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    #mongodb+srv://gustavopaterno:<db_password>@fitness.uioew9c.mongodb.net/?retryWrites=true&w=majority&appName=Fitness
    # Acess Local
    MONGODB_DATABASE_URI = 'mongodb+srv://gustavopaterno:G6Rf5Q3npCsgMHgq@fitness.uioew9c.mongodb.net/?retryWrites=true&w=majority&appName=Fitness'
    DATABASE_NAME = "Fitness"