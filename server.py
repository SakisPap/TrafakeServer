from flask import Flask, session, render_template, request
from flask_restplus import Api, Resource, fields
from toolbox import *


# Flag to enable/disable werkzeug debugger
RUN_WERKZEUG = True

# Flask app and api declarations
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api(app, version='1.0', title='Trafake Server API',
    description='Endpoints - register | login | submiturl | getPool | resetPool')


if not RUN_WERKZEUG:
    import logging
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True


a_register = api.model('Register', {'username':  fields.String(), 'password': fields.String()})
a_login = api.model('Login', {'username':  fields.String(), 'password': fields.String()})
a_url = api.model('AddToPool', {'username':  fields.String(), 'password': fields.String(), 'url':  fields.String()})
a_auth_request = api.model('Authenticate', {'username':  fields.String(), 'password': fields.String()})



@app.route('/status', methods=['GET','POST'])
def index():
    pool = returnUrlsOnly(urlPool)
    urlPool_arrayConvert = []
    print(urlPool)
    for item in urlPool:
        item = json.loads(item)
        urlPool_arrayConvert.append([item['user'], item['url']])

    return render_template("index.html", text=urlPool_arrayConvert)



@api.route('/register')
class Register(Resource):
    @api.expect(a_register)
    def post(self):
        print(" [API] Got user registration request ")
        username = api.payload['username']
        password = passwordHasher(api.payload['password'])
        if not checkIfUserExists(username):
           registerUser(username=username, password=password)
           return {'token': 'registrationSuccessful'}, 200

        else:
            return {'status': 'alreadyRegistered'}, 200


@api.route('/login')
class Session(Resource):
    @api.expect(a_login)
    def post(self):
        username = api.payload['username']
        password = passwordHasher(api.payload['password'])
        print(" [API] Got user session request ")
        if checkIfUserExists(username):
            if loginUserCheck(username=username, password=password):
                return {'status': 'loginSuccess'}, 200
            else:
                return {'status': 'wrongCreds'}, 500
        else:
            return {'status': 'wrongCreds'}, 500


@api.route('/submiturl')
class Session(Resource):
    @api.expect(a_url)
    def post(self):
        url = api.payload['url']
        username = api.payload['username']
        password = passwordHasher(api.payload['password'])
        print(" [API] Got submit url request ")
        if authenticateUser(username, password):
            if (url not in returnUrlsOnly(urlPool)) and (username not in returnUsersOnly(urlPool)):
                urlPool.append(json.dumps({"user": username, "url": url}))
            return {'status': 'submissionSuccess'}, 200
        else:
            return {'status': 'notInSession'}, 500


@api.route('/getPool')
class Session(Resource):
    @api.expect(a_auth_request)
    def post(self):
        username = api.payload['username']
        password = passwordHasher(api.payload['password'])
        if authenticateUser(username, password):
            pool = returnUrlsOnly(urlPool)
            return {'pool': pool}, 200
        else:
            return {'status': 'notInSession'}, 500


@api.route('/resetPool')
class Session(Resource):
    @api.expect(a_auth_request)
    def post(self):
        username = api.payload['username']
        password = passwordHasher(api.payload['password'])
        if authenticateUser(username, password):
            try:
                for row in urlPool:
                    if json.loads(row)["user"] == username:
                        urlPool.remove(row)
            except Exception as e:
                print(e)
            return {'status': 'resetSuccessful'}
        else:
            return {'status': 'notInSession'}, 500


if __name__ == '__main__':

    conn = sqlite3.connect('users.db')
    def createtable():
        conn.execute('''CREATE TABLE USERS (USERNAME CHAR(128) PRIMARY KEY NOT NULL, PASSWORD CHAR(128));''')

    try:
        createtable()
    except:
        print("Database users already exists; skipping creation")

    urlPool = []

    app.run(debug=True, host='0.0.0.0', port=5555)