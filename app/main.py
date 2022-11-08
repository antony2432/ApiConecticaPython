from flask import Flask, jsonify, request
import ros_api

app = Flask(__name__)


# * ApiMikrotik:
router = ros_api.Api('172.19.19.67', user='antony',
                     password='123456', port=8728)


# * Routes:
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenido'})


@app.route('/products', methods=['GET'])
def productos():
    return jsonify([{'Product': 'Laptop', 'Description': 'Esta es una laptop', 'quantity': 34}])


@app.route('/clientesActivo', methods=['GET'])
def clientes():
  try:
    return router.talk('/ppp/secret/print')
  except Exception as ex:
    return 'error'

@app.route('/clientesActivo', methods=['POST'])
def AgregarClientes():
  try:
    print(request.json)
    message = [('/ppp/secret/add', '=name='+request.json['name'], '=password='+request.json['password'],'=profile='+request.json['profile'], '=service=pppoe', '=comment='+request.json['comment'])]
    router.talk(message)
    return 'recibido'
  except Exception as ex:
      return 'error'

@app.route('/cliente/desactivar/<string:client_name>', methods=['GET'])
def clientDesable(client_name):
  try:
    disableSecret = [('/ppp/secret/disable\n=numbers='+client_name)]
    router.talk(disableSecret)
    return 'Supendido de forma correcta'
  except Exception as ex:
    return 'Error'

if __name__ == "__main__":
  app.run(debug=True)