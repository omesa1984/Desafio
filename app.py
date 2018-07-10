from flask import Flask
from flask import request
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import collections
import json
import json.decoder
import json.encoder
import pyodbc


app = Flask(__name__)

conn = pyodbc.connect(
    'DRIVER={SQL Server Native Client 11.0};'
    'SERVER=SQL5013.site4now.net;'
    'DATABASE=DB_9BBD5B_contactosdb;'
    'UID=DB_9BBD5B_contactosdb_admin;'
    'PWD=c0nt4ct0sdb'
)

# procura os dados solicitados pelos diferentes GET
def list_contacts(size, page, idContact):
    objects_list = []
    cont = 0
    for row in rows:
        if(size == 0 and page == 0 and idContact == -1):
            d = collections.OrderedDict()
            d['id'] = row.Id
            d['nome'] = row.Nome
            d['canal'] = row.Canal
            d['valor'] = row.Valor
            d['obs'] = row.Obs
            objects_list.append(d)
        else:
            if((idContact == -1) and (size > 0 or page > 0)):
                cont = cont + 1
                if (cont > (size * page)):
                    d = collections.OrderedDict()
                    d['id'] = row.Id
                    d['nome'] = row.Nome
                    d['canal'] = row.Canal
                    d['valor'] = row.Valor
                    d['obs'] = row.Obs
                    objects_list.append(d)
            else:
                if (idContact == row.Id):
                    d = collections.OrderedDict()
                    d['id'] = row.Id
                    d['nome'] = row.Nome
                    d['canal'] = row.Canal
                    d['valor'] = row.Valor
                    d['obs'] = row.Obs
                    objects_list.append(d)
                    break
        j = json.dumps(objects_list)

    return j

# Valida os String
def validate_dados(dado):
    if(dado.Nome.isalmu() and dado.Canal.isalmu() and dado.Valor.isalmu()):
        return True
    else:
        return False

# Valida os tipos de Canal
def validate_valor(canal, valor):
    if(canal.lower() == 'email'):
        return True
    else:
        if(((canal.lower() == 'celular') or (canal.lower() == 'fixo')) and canal.isdigit()):
            return True
        else:
            return False

# pagina inicial
@app.route('/')
def index():
    return 'Index Page'

# GET default, procura todos os contatos
@app.route('/get', methods=['GET'])
def get():

    cursor = conn.cursor()
    cursor.execute("select * from Contacts")
    rows = cursor.fetchall()

    j = list_contacts(0, 0, -1)

    conn.close()

    if not j:
        abort(401)
    else:
        return j

# GET que procura os contatos mas começa segun os parametros size e page
@app.route('/get', methods=['GET'])
def get_all(size, page):

    cursor = conn.cursor()
    cursor.execute("select * from Contacts")
    rows = cursor.fetchall()

    j = list_contacts(size, page, -1)

    conn.close()

    if not j:
        abort(401)
    else:
        return j

# GET procura um contato determinado
@app.route('/get', methods=['GET'])
def get_idContact(idContact):

    cursor = conn.cursor()
    cursor.execute("select * from Contacts where idContact == Contacts.Id")
    rows = cursor.fetchall()

    j = list_contacts(0, 0, idContact)

    conn.close()

    if not j:
        abort(401)
    else:
        return j

@app.route('/put/<int:idContato>', methods=['PUT'])
def update(idContato, dado):
    if(((idContato == None) or (dado == None)) or ((validate_dados(dado) == True) and (validate_valor(dado.Canal, dado.Valor) == True))):
        abort(204)
    else:
        cursor = conn.cursor()
        cursor.execute("UPDATE Contacts SET Contacts.Nome = dado.Nome, Contacts.Canal = dado.Canal,"
                       "Contacts.Valor = dado.Valor, Contacts.Obs = dado.Obs")
        conn.close()
        return 'The Contact is updated'

# Inserta um elemento nao banco de dados
@app.route('/post', methods=['POST'])
def insert(dado):
    if((dado == None) and ((validate_dados(dado) == True) and (validate_valor(dado.Canal, dado.Valor) == True))):
        abort(201)
    else:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO * FROM Contacts VALUES(dado.nome, dado.canal, dado.valor, dado.Obs)")
        conn.close()
        return 'The Contact is inserted'

# Apaga um contato com o ID enviado por parametro
@app.route('/delete/<int:idContato>')
def delete(idContato):
    if(idContato == None):
        abort(204)
    else:
        cursor = conn.cursor()
        cursor.execute("DELETE * FROM Contacts WHERE Contacts.Id = idContato")
        conn.close()
        return 'The Contact is deleted'





if __name__ == '__main__':
    app.run()
