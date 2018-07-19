"""
Copyright (c) 2018, Ankit R. Gadiya
BSD 3-Clause License
"""

from random import choice
from flask import Flask, request, Response
from sqlite3 import connect

"""
Configurations
"""
DB_NAME = "nnpy.db"
VALID_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ID_LEN = 5
BASE_URL = "http://example.com/"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response('Paste', mimetype='text/plain')
    elif request.method == 'POST':
        data = request.form['c']
        db = connect(DB_NAME)
        dbCursor = db.cursor()

        valid = False
        while not valid:
            pasteId = ""
            for i in range(ID_LEN):
                pasteId += choice(VALID_CHARS)

            query = dbCursor.execute("SELECT data FROM pastes WHERE id = '%s'" % pasteId)
            if len(query.fetchall()) == 0:
                valid = True

        paste = (pasteId, data)
        dbCursor.execute("INSERT INTO pastes VALUES (?, ?)", paste)
        db.commit()
        db.close()
        return BASE_URL + pasteId + '\n'

@app.route("/<pasteId>")
def paste(pasteId):
    if len(pasteId) != ID_LEN:
        return Response('Invalid ID', mimetype='text/plain')
    else:
        db = connect(DB_NAME)
        dbCursor = db.cursor()
        query = dbCursor.execute("SELECT data FROM pastes WHERE id = '%s'" % pasteId)
        data = query.fetchone()
        db.close()
        if data == None:
            return Response('Not Found',  mimetype='text/plain')
        else:
            return Response(data, mimetype='text/plain')
