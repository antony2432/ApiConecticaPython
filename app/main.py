from flask import Flask, jsonify, request
import ros_api
from routeros import login

app = Flask(__name__)


# * ApiMikrotik:
def getConectionMikro():
    return ros_api.Api('172.19.19.67', user='antony', password='123456', port=8728)


def getConectionOs():
    return login('antony', '123456', '172.19.19.67')

# * Routes:


@app.route('/conectica/apiv1', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenido'})


@app.route('/conectica/apiv1/clientes', methods=['GET'])
def getClients():
    try:
        routeros = getConectionOs()
        secretClients = routeros(('/ppp/secret/print'))
        print()
        return jsonify(
            {
                "totalClientes": len(secretClients),
                "clientes": secretClients
            }
        )
    except Exception as ex:
        print(ex)
        return 'error'


@app.route('/conectica/apiv1/cliente/agregar', methods=['POST'])
def addClient():
    try:
        router = getConectionMikro()
        print(request.json)
        message = [('/ppp/secret/add', '=name='+request.json['name'], '=password='+request.json['password'],
                    '=profile='+request.json['profile'], '=service=pppoe', '=comment='+request.json['comment'])]
        router.talk(message)
        return 'recibido'
    except Exception as ex:
        print(ex)
        return 'error'


@app.route('/conectica/apiv1/cliente/desactivar', methods=['POST'])
def disableClient():
    try:
        routeros = getConectionOs()
        routeros('/ppp/secret/disable', '=numbers=' + request.json['usuario'])
        activeClientName = routeros.query(
            '/ppp/active/print').equal(name=request.json['usuario'])
        message = request.json['usuario'] + ' supendido de forma correcta'
        if (len(activeClientName) != 0):
            searchClient = routeros.query(
                '/ppp/active/print').equal(name=request.json['usuario'])
            routeros('/ppp/active/remove', '=numbers='+searchClient[0]['.id'])
        else:
            routeros.close()
            return message
        routeros.close()
        return message
    except Exception as ex:
        print(ex)
        return 'Error'


@app.route('/conectica/apiv1/cliente/nombre/<string:client_dni>', methods=['GET'])
def getClientForUser(client_dni):
    try:
        routeros = getConectionOs()
        secretClient = routeros.query(
            '/ppp/secret/print').equal(name=client_dni)
        if (len(secretClient) != 0):
            routeros.close()
            return secretClient[0]
        else:
            routeros.close()
            return jsonify({'message': 'Cliente no encontrado'})
    except Exception as ex:
        print(ex)
        return 'error'


@app.route('/conectica/apiv1/cliente/activos', methods=['GET'])
def getActiveCustomers():
    try:
        routeros = getConectionOs()
        ActiveClients = routeros('/ppp/active/print')
        routeros.close()
        return jsonify(
            {
                "totalClientes": len(ActiveClients),
                "clientes": ActiveClients
            }
        )
    except Exception as ex:
        print(ex)
        return 'Error'

@app.route('/conectica/apiv1/cliente/activar', methods=['POST'])
def actiivateClient():
    pass


if __name__ == "__main__":
    app.run(host="172.19.19.40", debug=True, port=3030)
