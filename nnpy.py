"""
Copyright (c) 2018, Ankit R. Gadiya
BSD 3-Clause License
"""

from flask import Flask, request, Response, redirect
from random import sample
import re
from sqlite3 import connect
from string import ascii_letters, digits

# Configurations
DB_NAME = "nnpy.db"
VALID_CHARS = ascii_letters + digits
ID_LEN = 5
URL_REGEX = re.compile('^https?:\/\/([a-zA-Z0-9\-]+\.)+[a-zA-Z0-9\-]+(\/[^\s]*)?$')

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return Response('Paste', mimetype='text/plain')
    elif request.method == 'POST':
        data = request.form['c']
        db = connect(DB_NAME)
        dbCursor = db.cursor()

        while True:
            pasteId = ''.join(sample(VALID_CHARS, ID_LEN))

            query = dbCursor.execute("SELECT data FROM pastes WHERE id = '{}'".format(pasteId))
            if len(query.fetchall()) == 0:
                break

        dbCursor.execute("INSERT INTO pastes VALUES (?, ?)", (pasteId, data))
        db.commit()
        db.close()
        return request.url_root + pasteId + '\n'

@app.route("/<pasteId>")
def paste(pasteId):
    if len(pasteId) != ID_LEN:
        return Response('Invalid ID', mimetype='text/plain')
    else:
        db = connect(DB_NAME)
        dbCursor = db.cursor()
        query = dbCursor.execute("SELECT data FROM pastes WHERE id = '{}'".format(pasteId))
        data = query.fetchone()
        db.close()
        if data == None:
            return Response('Not Found',  mimetype='text/plain')
        else:
            if re.match(URL_REGEX, data[0]) is not None:
                return redirect(data[0].strip(), code=302)
            else:
                return Response(data[0], mimetype='text/plain')

if __name__ == "__main__":
    app.run()
