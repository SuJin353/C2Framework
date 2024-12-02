from flask import Blueprint, render_template, redirect, request, url_for
import flask
import os
agents_bp = Blueprint('agents', __name__, template_folder='templates', static_folder='static')


class Agent:

    def __init__(self, name, listener, type, remote_address, remote_port):

        self.name = name
        self.listener = listener
        self.type = type
        self.remote_address = remote_address
        self.remote_port = remote_port
        self.sleep = 3
        self.path = f"database/listeners/{self.listener}/{self.name}"

@agents_bp.route('/', methods=['GET','POST'])
def agents():
    if request.method == 'POST':
        remote_address = flask.request.remote_addr
        hostname = flask.request.form.get("name")
        type = flask.request.form.get("type")
        print('agent checked in', remote_address, hostname, type)

    return render_template('agents.html')






