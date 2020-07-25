from flask import Flask,render_template, request, Response, redirect
from database import connector
from model import entities
import json
#from flask import session as gsession
gsession = {}
from datetime import datetime

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/static/<content>', methods=['GET','POST','PUT','DELETE'])
def static_content(content):
    return render_template(content)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

@app.route('/catalogo')
def catalogo():
    return render_template('cata    logo.html')

@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users', methods = ['POST'])
def create_user():
    data =json.loads(request.data)
    user = entities.User(
        username=data['username'],
        name=data['name'],
        fullname=data['fullname'],
        password=data['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    response = {'user': 'created'}
    return Response(json.dumps(response, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')

@app.route('/envmensaje', methods = ['POST'])
def envmessage():
    data =json.loads(request.data)
    mensaje = entities.Mensaje(
        nombre=data['Nombre'],
        email=data['email'],
        phone=data['phone'],
        message=data['message']
    )
    session = db.getSession(engine)
    session.add(mensaje)
    session.commit()
    response = {'Mensaje': 'created'}
    return Response(json.dumps(response, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')


@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'


@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(users)
    session.commit()
    return "Deleted User"


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')


@app.route('/compras', methods = ['GET'])
def get_compra():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Compras)
    data = []
    for compra in dbResponse:
        data.append(compra)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/compras', methods = ['POST'])
def create_compra():
    c =  json.loads(request.form['values'])
    compra = entities.Compras(
        usercomprador_id=c['usercomprador']['username']['id'],
        producto_id=c['producto']['nombre']['id'],
        satisfaccion=c['satisfaccion']
    )
    session = db.getSession(engine)
    session.add(compra)
    session.commit()
    return 'Created Compra'

@app.route('/compras', methods = ['DELETE'])
def delete_compra():
    id = request.form['key']
    session = db.getSession(engine)
    compras = session.query(entities.Compras).filter(entities.Compras.id == id).one()
    session.delete(compras)
    session.commit()
    return "Deleted Compras2"


@app.route('/compras', methods = ['PUT'])
def update_compra():
    session = db.getSession(engine)
    id = request.form['key']
    compra = session.query(entities.Compras).filter(entities.Compras.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(compra, key, c[key])
    session.add(compra)
    session.commit()
    return 'Updated User'

@app.route('/compras/<user_from_id>/<user_to_id>', methods = ['PUT'])
def compra():
    session = db.getSession(engine)
    id = request.form['key']
    compra = session.query(entities.Compras).filter(entities.Compras.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(compra, key, c[key])
    session.add(compra)
    session.commit()
    return 'Updated User'


@app.route('/compra', methods = ["POST"])
def comprar():
    data = json.loads(request.data)
    usercomprador_id = data['usercomprador_id']
    producto_id = data['producto_id']
    satisfaccion = data['satisfaccion']

    newcompra = entities.Compras(
    usercomprador_id = usercomprador_id,
    producto_id = producto_id,
    satisfaccion = satisfaccion)

    #2. Save in database
    db_session = db.getSession(engine)
    db_session.add(newcompra)
    db_session.commit()


@app.route('/mobile/productos', methods = ['GET'])
def get_mobileprooducto():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Producto)
    data = []
    for producto in dbResponse:
        data.append(producto)
    message = {'response' : data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')


@app.route('/productos', methods = ['GET'])
def get_productos():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Producto)
    data = []
    for producto in dbResponse:
        data.append(producto)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/productos', methods = ['POST'])
def create_productos():
    c =  json.loads(request.form['values'])
    producto = entities.Producto(
        codigo=c['codigo'],
        nombre=c['nombre'],
        marca=c['marca'],
        cantidad=c['cantidad'],
        precio=c['precio'],

    )
    session = db.getSession(engine)
    session.add(producto)
    session.commit()
    return 'Created producto'


@app.route('/productos', methods = ['PUT'])
def update_producto():
    session = db.getSession(engine)
    id = request.form['key']
    producto = session.query(entities.Producto).filter(entities.Producto.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(producto, key, c[key])
    session.add(producto)
    session.commit()
    return 'Updated User'


@app.route('/productos', methods = ['DELETE'])
def delete_producto():
    id = request.form['key']
    session = db.getSession(engine)
    productos = session.query(entities.Producto).filter(entities.Producto.id == id).one()
    session.delete(productos)
    session.commit()
    return "Deleted Compras"

@app.route("/authenticate", methods=['POST'])
def authenticate():
    message=json.loads(request.data)

    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.username == message['username']
    ).filter(
        entities.User.password == message['password']
    )
    user_l = user[:]
    db_session.close()
    if user_l != None:
        print('entro al if')
        gsession["user"]=json.dumps(user_l,cls=connector.AlchemyEncoder)
        print(gsession)
        print(gsession["user"])
        loge={"respuesta":"Logueado","id":user_l[0].id,"username":user_l[0].username}
        return Response (json.dumps(loge,cls=connector.AlchemyEncoder ),status=200,mimetype="application/json")
    else:
        loge ={"respuesta" :" Sorry " + message['username'] + " you are not a valid user"}
        return Response (json.dumps(loge,cls=connector.AlchemyEncoder ),status=202,mimetype="application/json")


@app.route('/current', methods = ["GET"])
def current_user():
    gsession['asd'] = 'gaaaaaaaa'
    print(gsession)
    print(gsession)
    print(gsession)
    db_session = db.getSession(engine)
    x = json.loads(gsession["user"])
    print(x)
    user = db_session.query(entities.User).filter(
        entities.User.id == x[0]["id"]
        ).first()

    return Response(json.dumps(
            user,
            cls=connector.AlchemyEncoder),
            mimetype='application/json'
        )

@app.route('/logout', methods = ["GET"])
def logout():
    session.clear()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

