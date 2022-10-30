import nltk
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import create_access_token
from flask_restful import Resource, Api, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import get_jwt
from sqlalchemy import create_engine
from flask import Flask, Response
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import datetime
import random
import string
import ast
import re
import os


# --- API Configurations----------------------------------------------------------------------------------------------
app = Flask(__name__)
api = Api(app)

load_dotenv()
db_uri = os.getenv("DB_URI", "")

engine = create_engine(db_uri)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=15000)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
jwt = JWTManager(app)
parser = reqparse.RequestParser()


# --- Helper Functions / Classes --------------------------------------------------------------------------------------
def get_conn1():
    database = os.getenv("DB_name", ""),
    user = os.getenv("User", ""),
    password = os.getenv("Password", ""),
    host = os.getenv("Endpoint", ""),
    port = os.getenv("Port", "")
    conn1 = psycopg2.connect(
        database=os.getenv("DB_name", ""),
        user=os.getenv("User", ""),
        password=os.getenv("Password", ""),
        host=os.getenv("Endpoint", ""),
        port=os.getenv("Port", "")
    )
    return conn1


class Encryption():
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


# --- Generic Endpoints ----------------------------------------------------------------------------------------------
@app.route('/healthy')
def healthy():
    return "OK", 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blocklist_df = pd.DataFrame(
            {'jti': [jti]})
        blocklist_df.to_sql("blocklist", con=db.engine, if_exists='append', index=False)
        return {"status": 200, "result": "The User has been logged out"}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return Response('{"status": 400, "result": "Token expired"}', status=400, mimetype='application/json')


@jwt.token_in_blocklist_loader
def check_token_in_blocklist(jwt_header, jwt_data):
    blocklist_df = pd.read_sql_table('blocklist', engine)
    blocklist = blocklist_df["jti"].tolist()
    return jwt_data["jti"] in blocklist


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return {"status": 400, "result": "The token has been revoked"}


# --- Specific Endpoints ----------------------------------------------------------------------------------------------
class login(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('email', required=True)  # add args
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user_df = pd.read_sql_table('users', engine)
        user_row = user_df[user_df["email"] == args["email"]]
        if len(user_row) != 1:
            return {"status": 404, "result": "wrong email"}

        if Encryption.verify_hash(args["password"], user_row["password"].item()):
            # if user_row["email_confirmed"].item() != True:
            #     return {"status": 404, "result": "Email address has not been confirmed"}

            user_id = user_row["user_id"].item()
            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)

            return {"status": 200, "result": {
                                            'message': 'Logged in as {}'.format(user_id),
                                            'access_token': access_token,
                                            'refresh_token': refresh_token,
                                            }}
        else:
            return {"status": 404, "result": "Wrong credentials"}


def check_password(password):
    pw_df = pd.read_sql_table("special_data_pw", engine)
    pw = pw_df["password"].item()

    if pw == password:
        return True
    else:
        return False


# --- User Management -------------------------------------------------------------------------------------------------
class personal_data(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user_df = pd.read_sql_table('users', engine)
        personal_user_df = user_df[user_df["user_id"] == user_id]

        first_name = personal_user_df["first_name"].item()
        last_name = personal_user_df["last_name"].item().replace("?", "'")
        email = personal_user_df["email"].item().replace("?", "'")

        output = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
        return {"status": 200, "result": output} # return data and 200 OK code

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('first_name', required=True)  # add args
        parser.add_argument('last_name', required=True)  # add args
        parser.add_argument('email', required=True)  # add args
        parser.add_argument('password', required=True)  # add args

        args = parser.parse_args()  # parse arguments to dictionary

        password = args["password"]
        flag = 0
        while True:
            if (len(password) < 8):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[!@#$%^&*()-+?_=,<>/]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                break

        if flag == -1:
            return {"status": 404, "result": "No secure password"}

        registration_date = datetime.datetime.today()

        user_df = pd.read_sql_table('users', engine)

        email_list = user_df['email'].tolist()
        if args["email"] in email_list:
            return {"status": 404, "result": "This email is already in use"}

        user_id_list = user_df['user_id'].tolist()
        user_id = get_patient_id()
        while user_id in user_id_list:
            user_id = get_patient_id()

        enc_password = Encryption.generate_hash(args["password"])

        user_df = pd.DataFrame(
            {'user_id': [user_id], 'first_name': [args["first_name"].replace("?", "'")], 'last_name': [args["last_name"].replace("?", "'")],
             'email': [args["email"]], 'password': [enc_password], 'registration_date': [registration_date]})
        user_df.to_sql("users", con=db.engine, if_exists='append', index=False)

        return {"status": 200, "result": "User has been registered"}


def get_patient_id():
    length = 8
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)

# --- Hackathron -------------------------------------------------------------------------------------------------------

def update_db(DB_TABLE, DB_INDEX_COLUMN, new_dataset):
    try:
        db = pd.read_sql_table(DB_TABLE, engine)
    except ValueError:
        db = pd.DataFrame(
            columns=[DB_INDEX_COLUMN, *list(new_dataset.keys())])

    db.loc[len(db[DB_INDEX_COLUMN]), DB_INDEX_COLUMN] = len(db[DB_INDEX_COLUMN])
    for key, value in new_dataset.items():
        db.loc[len(db[key]) - 1, key] = value

    db[DB_INDEX_COLUMN] = db[DB_INDEX_COLUMN].astype(int)

    res = db.to_sql(DB_TABLE, con=engine, if_exists='replace', index=False)
    return res

def name_to_id(tdict):
    person = 'patient'
    db = pd.read_sql_table(person, engine)
    patient_Id = -1
    temp = tdict[f'{person}Name']
    dict_vorname = temp[:temp.find(' ')]
    dict_nachname = temp[temp.find(' ') + 1:]
    best_distance = 100000
    bes_index = -1
    for idx, row in db.iterrows():
        db_vorname = row['pfName']
        db_nachname = row['psName']
        d1 = nltk.edit_distance(db_vorname, dict_vorname)
        d1 += nltk.edit_distance(db_nachname, dict_nachname)
        d2 = nltk.edit_distance(db_vorname, dict_nachname)
        d2 += nltk.edit_distance(db_nachname, dict_vorname)

        if best_distance > d1:
            best_distance = d1
            best_index = row['patientID']

        if best_distance > d2:
            best_distance = d2
            best_index = row['patientID']

    if best_distance <= 2:
        try:
            tdict[f'{person}ID'] = best_index
            tdict.pop(f'{person}Name')
        except:
            return False


    return tdict

class post_initialize_vitalsTypes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        args = parser.parse_args()

        vitals_dict = {
            'vitName': ['Herzfrequenz',
                        'BlutdruckSYS',
                        'BlutdruckDIA',
                        'Körpertemperatur',
                        'Gewicht',
                        'Atemfrequenz',
                        'Sauberstoffsättigung',
                        'Blutzucker',
                        'Erythrozyten',
                        'Leukozyten',
                        'Thrombozyten',
                        'Hämatokritit',
                        'Hämoglobin',
                        'Cholesterin',
                        'Schmerzempfinden',
                        'Braden-Score',
                        'Brass-Index',
                        'Bienstein-Skala',
                        'Stuhlausscheidung',
                        'Flüssigkeitsaufnahme',
                        'Größe',
                        'Sturz'
                        ],
            'vitUnit': ['1/min',
                        'mmHg',
                        'mmHg',
                        '°C',
                        'kg',
                        '1/min',
                        '%',
                        'mg/dl',
                        'tpt/l',
                        'Zellen/µl',
                        '10⁹/l',
                        '%',
                        'mg/dl',
                        'mg/dl',
                        '1 - 10',
                        '1 - 4',
                        '0 - 4',
                        '0 - 3',
                        'kg',
                        'ml',
                        'm',
                        'Stück'
                        ]
        }
        temp = []
        for i in range(len(vitals_dict['vitName'])):
            temp.append(i)
        vitals_dict['vitType'] = temp

        vitalsTypes = pd.DataFrame(vitals_dict)

        res = vitalsTypes.to_sql(f'vitalsTypes', con=engine, if_exists='replace', index=False)

        return {"status": 200, "result": "Data has been added."}

class post_initialize_rooms(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rooms_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['rooms_dict'])

        update_db('rooms', 'roomId', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_new_patient(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['patient_dict'])

        update_db('patient', 'patientID', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_new_employee(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['employee_dict'])

        update_db('employee', 'employeeID', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_new_prescriptions(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prescriptions_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['prescriptions_dict'])

        new_data = name_to_id(new_data)
        if isinstance(new_data, bool):
            if new_data == False:
                return {"status": 400, "result": "Es tut mit leid, mir ist kein Patient mit diesem Namen bekannt."}
        update_db('prescriptions', 'prescId', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_new_patientRequest(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patientRequest_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['patientRequest_dict'])

        new_data = name_to_id(new_data)
        if isinstance(new_data, bool):
            if new_data == False:
                return {"status": 400, "result": "Es tut mit leid, mir ist kein Patient mit diesem Namen bekannt."}
        update_db('patientRequest', 'pReqId', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_update_medication(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('medication_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['medication_dict'])

        new_data = name_to_id(new_data)
        if isinstance(new_data, bool):
            if new_data == False:
                return {"status": 400, "result": "Es tut mit leid, mir ist kein Patient mit diesem Namen bekannt."}
        update_db('medication', 'medId', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_update_vitals(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('vitals_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['vitals_dict'])

        new_data = name_to_id(new_data)
        if isinstance(new_data, bool):
            if new_data == False:
                return {"status": 400, "result": "Es tut mit leid, mir ist kein Patient mit diesem Namen bekannt."}
        update_db('vitals', 'vitID', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_update_patientcondition(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patientcondition_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['patientcondition_dict'])

        new_data = name_to_id(new_data)
        if isinstance(new_data, bool):
            if new_data == False:
                return {"status": 400, "result": "Es tut mit leid, mir ist kein Patient mit diesem Namen bekannt."}
        update_db('patientcondition', 'pcId', new_data)

        return {"status": 200, "result": "Data has been added."}

class post_update_roomConditions(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roomConditions_dict', required=True)
        args = parser.parse_args()
        new_data = ast.literal_eval(args['roomConditions_dict'])

        update_db('roomConditions', 'roomId', new_data)

        return {"status": 200, "result": "Data has been added."}


#--- Routes -----------------------------------------------------------------------------------------------------------
api.add_resource(TokenRefresh, '/token_refresh')
api.add_resource(personal_data, '/personal_data')
api.add_resource(login, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(post_initialize_vitalsTypes, '/post_initialize_vitalsTypes')
api.add_resource(post_initialize_rooms, '/post_initialize_rooms')

api.add_resource(post_new_patient, '/post_new_patient')
api.add_resource(post_new_employee, '/post_new_employee')
api.add_resource(post_new_prescriptions, '/post_new_prescriptions')
api.add_resource(post_new_patientRequest, '/post_new_patientRequest')

api.add_resource(post_update_medication, '/post_update_medication')
api.add_resource(post_update_vitals, '/post_update_vitals')
api.add_resource(post_update_patientcondition, '/post_update_patientcondition')
api.add_resource(post_update_roomConditions, '/post_update_roomConditions')


#--- Run/Serve app ----------------------------------------------------------------------------------------------------
if __name__ =='__main__':
    print('Api started')
    app.run(debug=True, host='0.0.0.0')
