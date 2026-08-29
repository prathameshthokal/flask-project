from flask import render_template,redirect,url_for,flash,request,jsonify
from grocerylist import app, db, bcrypt

@app.route('/ping')
def ping():
    return jsonify({'status': 'ok'})
