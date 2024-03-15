from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 


###Importar la configuracion 
from .config import Config

##### Crenando el objetyo de aplicacion ##
app = Flask(__name__)

#### Configurando el objeto flask con el config 
app .config.from_object(Config)

## Creando el objeto SQLALchemy --> perrmite hacer entidades 

db = SQLAlchemy(app)
##creo el objeto para hacer migraciones 
migrate = Migrate(app, db)

##importando rutas 

from . import routes 

## Importando los modelos  
from .models import Medico, Paciente, Consultorio, Cita

####Ejecutando el objeto ##
if __name__ == '__main__':
    app.run()
