from flask import Flask, render_template, request,redirect,url_for
from sqlalchemy import text
import numpy as np
import matplotlib.pyplot as plt
import db
from models import tipoUsuario,producto,proveedores
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verificar",methods=["POST"])
def comprobar():
    nombre=request.form["nombreUsuario"]
    contraseña=request.form["contra"]
    print("Su nombre es: ",nombre,"Contraseña: ",contraseña)
    a=db.session.query(tipoUsuario).filter_by(nombreCompleto= nombre).first()
    if a is None:
        return "No existente"
    else:
        if a.contraseña == contraseña:
            if a.tipo==False:
                todos_los_productos = db.session.query(producto).all()
                for i in todos_los_productos:
                    print(i)
                return render_template("customers.html",lista_productos=todos_los_productos)
            else:
                a = db.session.query(producto).all()
                sobrepasado = []
                for i in a:
                    print(i.nombreDelProducto)
                    respuesta = (i.cantidadTotal * 90) / 100
                    print(respuesta)
                    if respuesta <= i.cantidadVendida:
                        sobrepasado.append(i)
                        print(i.nombreDelProducto,"ya sobrepaso el 90%")
                return render_template("admin.html",lista_sobrepasado=sobrepasado)
        else:
            return "Contraseña incorrecta"
@app.route("/crear",methods=['GET','POST'])
def crear():
    if request.form.get("nombreNuevo") != None:
        nombre=request.form.get("nombreNuevo")
        contra=request.form.get("contraNueva")
        tip=request.form.get("opcion")
        if tip == "1":
            tip = True
        else:
            tip = False
       # print(nombre1,contraseña1,tipo1)
        nuevo=tipoUsuario(nombreCompleto=nombre, contraseña=contra,tipo=tip)
        db.session.add(nuevo)
        db.session.commit()
    return render_template("Crear.html")
@app.route("/inventario")
def inven():
    todos_los_productos=db.session.query(producto).all()
    for i in todos_los_productos:
        print(i)
    return render_template("inventario.html",lista_productos=todos_los_productos)
@app.route("/añadirproducto",methods=['GET','POST'])
def añadirproducto():
    if request.form.get("nombreproducto") != None:
        nombre=request.form.get("nombreproducto")
        cantidad=request.form.get("cantidad")
        precio=request.form.get("precio")
        ubicacion=request.form.get("ubicacion")
        imagen=request.form.get("imagen")
        print(nombre,cantidad,precio,ubicacion)
        p=producto(nombreDelProducto=nombre,cantidadDisponible=cantidad,cantidadTotal=cantidad,precio=precio,ubicacion=ubicacion,ganancias=0,cantidadVendida=0,imagen=imagen)
        print(p)
        db.session.add(p)
        produc = db.session.query(producto).order_by(producto.id_producto.desc()).first()
        print(produc.id_producto)
        produ_id = produc.id_producto
        produc = db.session.query(producto).order_by(producto.id_producto.desc()).first()
        print(produc.id_producto)
        produ_id = produc.id_producto
        nombre = request.form.get("nombreproveedor")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        print(nombre, telefono, email, produ_id)
        prove = proveedores(nombre=nombre, telefono=telefono, email=email, producto_id=produ_id)
        print(prove)
        db.session.add(prove)
        db.session.commit()
    return render_template("añadirProducto.html")
@app.route("/eliminar-producto/<id>" )
def eliminar(id):
    produc=db.session.query(producto).filter_by(id_producto=id).delete()
    provee=db.session.query(proveedores).filter_by(id=id).delete()
    db.session.commit()
    return redirect("/inventario")
@app.route("/menuadm")
def volveradm():
    a = db.session.query(producto).all()
    sobrepasado = []
    for i in a:
        print(i.nombreDelProducto)
        respuesta = (i.cantidadTotal * 90) / 100
        print(respuesta)
        if respuesta <= i.cantidadVendida:
            sobrepasado.append(i)
            print(i.nombreDelProducto, "ya sobrepaso el 90%")
    return render_template("admin.html",lista_sobrepasado=sobrepasado)
@app.route("/comprarproducto/<id>",methods=['GET','POST'])
def comprarproducto(id):
    product=db.session.query(producto).filter_by(id_producto=id).first()
    cantidadcomprada=request.form.get("cantidadAComprar")
    a=int(cantidadcomprada)
    cantidadAntigua=product.cantidadDisponible
    if a <= cantidadAntigua and a >= 1:
        vendidaAnterior=product.cantidadVendida
        product.cantidadVendida=vendidaAnterior+a
        gananciaAnterior=product.ganancias
        cantidadcomprada=float(cantidadcomprada)
        ganancia=cantidadcomprada*product.precio
        nuevoValor=gananciaAnterior+ganancia
        product.ganancias=nuevoValor
        cantidadNueva=cantidadAntigua-a
        product.cantidadDisponible=cantidadNueva
        db.session.commit()
        return render_template("comprarproducto.html")
    else:
        todos_los_productos = db.session.query(producto).all()
        return render_template("customers.html",lista_productos=todos_los_productos)
@app.route("/cliente")
def cliente():
    todos_los_productos = db.session.query(producto).all()
    cantidadcomprada = request.form.get("cantidadAComprar")
    for i in todos_los_productos:
        print(i)
    return render_template("customers.html",lista_productos=todos_los_productos)
@app.route("/proveedores")
def proveedor():
    todos_los_proveedores = db.session.query(proveedores).all()
    for i in todos_los_proveedores:
        print(i)
    return render_template("proveedores.html",lista_proveedores=todos_los_proveedores)
@app.route("/graficas")
def graficas ():

    a=db.session.query(producto).all()
    nombres=[]
    ganancias=[]
    for i in a:
        nombres.append(i.nombreDelProducto)
        ganancias.append(i.ganancias)
        print(i)
    print(nombres)
    fig, ax = plt.subplots()
    ax.bar(nombres, ganancias)
    ax.set_ylabel('GANANCIAS')
    ax.set_title('PRODUCTOS')

    plt.show()
    return render_template("admin.html")
@app.route("/cantidades")
def cantidades():
    a = db.session.query(producto).all()
    nombres = []
    cantidadTotal= []
    cantidadDisponible=[]
    for i in a:
        nombres.append(i.nombreDelProducto)
        cantidadTotal.append(i.cantidadTotal)
        cantidadDisponible.append(i.cantidadDisponible)
    cantidades_totales = {
        'Total': cantidadTotal,
        'Disponible': cantidadDisponible,
    }

    x = np.arange(len(nombres))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in cantidades_totales.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Cantidades')
    ax.set_title('Disponible vs Total')
    ax.set_xticks(x + width, nombres)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 250)

    plt.show()

    return render_template("admin.html")
@app.route("/estadisticascliente")
def estadisticasCliente():
    a = db.session.query(producto).all()
    nombres = []
    ventas = []
    for i in a:
        nombres.append(i.nombreDelProducto)
        ventas.append(i.cantidadVendida)
        print(i)
    print(nombres)
    fig, ax = plt.subplots()
    ax.bar(nombres, ventas)
    ax.set_ylabel('CANTIDADES VENDIDAS')
    ax.set_title('PRODUCTOS')

    plt.show()
    todos_los_productos = db.session.query(producto).all()

    return render_template("customers.html", lista_productos=todos_los_productos)
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
