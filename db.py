from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El engine permite a SQLAlchemy comunicarse con la base de datos
engine = create_engine('sqlite:///database/Usuarios.db', connect_args={'check_same_thread': False})
# crear el engine no conecta inmediatamente a la base de datos

# Ahora creamos la sesion, lo que nos permite realizar la transaccion dentro de nuestra base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Ahora vamos al fichero models.py y en los modelos (clases) donde queramos que se transformen en tablas le
# añadiremos esta variable y esto se encargara de vincular la clase a la tabla
Base = declarative_base()