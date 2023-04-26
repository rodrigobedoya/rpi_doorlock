from flask import Flask, render_template, session, request, jsonify, Response, redirect,url_for
from sqlalchemy import and_

from model import entities
from database import connector
import json
import datetime

app = Flask(__name__)
db = connector.Manager()

engine = db.createEngine()


doorlock_password = "key"
def addEvent(input_password):
    sessiondb = db.getSession(engine)
    if input_password==doorlock_password:
        event = entities.Event(
            type="door opened",
            time=datetime.datetime.utcnow()
        )
        sessiondb.add(event)
        sessiondb.commit()
        print("success")
    else:
        event = entities.Event(
            type="someone tried to open the door",
            time=datetime.datetime.utcnow()
        )
        sessiondb.add(event)
        sessiondb.commit()
        print("failure")

@app.route('/', methods = ['GET'])
def login():
    session['logged'] = ""
    session['position'] = ""
    return render_template("login.html")

@app.route('/static/<content>')
def static_content(content):
    if session["logged"] == "":
        return "You need to log in first"
    elif content =="crud_accounts.html":
        if session['position'] =="":
            return "You don't have access to this page"
    return render_template(content)

@app.route('/do_login', methods = ['POST'])
def do_login():
    name = request.form['name']
    password = request.form['password']
    sessiondb = db.getSession(engine)
    account = sessiondb.query(entities.Account).filter(
        and_(entities.Account.name == name, entities.Account.password == password )
    ).first()
    if account != None:
        session['logged'] = account.id
        session['position'] = account.position
        return "logged successfully"
    else:
        return redirect(url_for("login"))


@app.route('/accounts', methods = ['GET'])
def get_accounts():
    key = 'getAccounts'
    sessiondb = db.getSession(engine)
    accounts = sessiondb.query(entities.Account)
    data = []
    for account in accounts:
        data.append(account)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/accounts/<id>', methods = ['GET'])
def get_account(id):
    session = db.getSession(engine)
    accounts = session.query(entities.Account).filter(entities.Account.id == id)
    for account in accounts:
        js = json.dumps(account, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/accounts', methods = ['DELETE'])
def remove_account():
    id = request.form['key']
    session = db.getSession(engine)
    accounts = session.query(entities.Account).filter(entities.Account.id == id)
    for account in accounts:
        session.delete(account)
    session.commit()
    return "Deleted User"


@app.route('/accounts', methods = ['POST'])
def create_account():
    c =  json.loads(request.form['values'])
    #c = request.get_json(silent=True)
    print(c)
    account = entities.Account(
        position=c['position'],
        name=c['name'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(account)
    session.commit()
    return 'Created User'

@app.route('/accounts', methods = ['PUT'])
def update_account():
    session = db.getSession(engine)
    id = request.form['key']
    account = session.query(entities.Account).filter(entities.Account.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(account, key, c[key])
    session.add(account)
    session.commit()
    return 'Updated User'




#------------------------------------------


@app.route('/events', methods = ['GET'])
def get_events():
    key = 'getEvents'
    sessiondb = db.getSession(engine)
    events = sessiondb.query(entities.Event)
    data = []
    for event in events:
        data.append(event)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/events/<id>', methods = ['GET'])
def get_event(id):
    session = db.getSession(engine)
    events = session.query(entities.Event).filter(entities.Event.id == id)
    for event in events:
        js = json.dumps(event, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { "status": 404, "message": "Not Found"}
    return Response(message, status=404, mimetype='application/json')


@app.route('/events', methods = ['DELETE'])
def delete_event():
    id = request.form['key']
    session = db.getSession(engine)
    events = session.query(entities.Event).filter(entities.Event.id == id)
    for event in events:
        session.delete(event)
    session.commit()
    return "Deleted Message"


@app.route('/events', methods = ['POST'])
def create_event():
    #c =  json.loads(request.form['values'])
    c = request.get_json(silent=True)
    session = db.getSession(engine)
    event = entities.Event(
        type = c['type'],
        time = datetime.datetime.utcnow()
    )
    session.add(event)
    session.commit()
    return 'Created Message'

@app.route('/events', methods = ['PUT'])
def update_event():
    session = db.getSession(engine)
    id = request.form['key']
    event = session.query(entities.Event).filter(entities.Event.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(event, key, c[key])
    session.add(event)
    session.commit()
    return 'Updated Message'


if __name__ == '__main__':
    app.secret_key = ".."
    app.run()


