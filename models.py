from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
import db

class tipoUsuario (db.Base):
    __tablename__="usuario"
    __table_args__ = {'sqlite_autoincrement':True}
    id_usuario = Column(Integer,primary_key=True)
    nombreCompleto=Column(String(200))
    contraseña=Column(String(200))
    tipo=Column(Boolean)#0 para usuario 1 para Administrador

    def __init__(self,nombreCompleto,contraseña,tipo):
        self.nombreCompleto=nombreCompleto
        self.contraseña=contraseña
        self.tipo=tipo

    def __str__(self):
        return "Usuario:{}->{}->{}->{}".format(self.id_usuario,self.nombreCompleto,self.contraseña,self.tipo)
class producto(db.Base):
    __tablename__ = "producto"
    __table_args__ = {'sqlite_autoincrement': True}
    id_producto = Column(Integer, primary_key=True)
    nombreDelProducto = Column(String(200))
    cantidadDisponible = Column(Integer)
    cantidadTotal=Column(Integer)
    cantidadVendida=Column(Integer)
    precio = Column(Float)
    ubicacion=Column(String(200))
    ganancias=Column(Float,nullable=False)
    imagen=Column(String)


    def __int__(self,nombreDelProducto,cantidadTotal,cantidadDisponible,cantidadVendida,precio,ubicacion,imagen):
        self.nombreDelProducto=nombreDelProducto
        self.cantidadTotal=cantidadTotal
        self.cantidadDisponible=cantidadDisponible
        self.cantidadVendida=cantidadVendida
        self.precio=precio
        self.ubicacion=ubicacion
        self.imagen=imagen

    def __str__(self):
        return "{}->producto->{} cantidad->{} precio->{} ubicacion->{}".format(self.id_producto,self.nombreDelProducto,self.cantidadTotal,self.precio,self.ubicacion)



class proveedores(db.Base):
    __tablename__ = "proveedores"
    __table_args__ = {'sqlite_autoincrement': True}
    id=Column(Integer,primary_key=True)
    nombre=Column(String(200))
    telefono=Column(String(30))
    email=Column(String(200))
    producto_id=Column(Integer,ForeignKey('producto.id_producto'))

    def __int__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return "{}->nombre->{} telefono->{} email->{} ".format(self.id,self.nombre,self.telefono,self.email)
