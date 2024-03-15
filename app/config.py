import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    ##SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:@localhost/citas_2826502'
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir, "database.db")
    SQLALCHEMY_TRACK_NOTIFICATION=True
    SECRET_KEY = 'vistas'
    
