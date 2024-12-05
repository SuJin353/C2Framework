from flask import Flask, Blueprint, render_template, redirect, request, url_for
from .edit_listener import EditListener

import threading
import os
import socket
import json
import flask

from multiprocessing import Process

listeners_bp = Blueprint('listeners', __name__, template_folder='templates', static_folder='static')

class Listener:

    def __init__(self, name, type, bind_address, bind_port):

        self.name = name
        self.type = type
        self.bind_address = bind_address
        self.bind_port = bind_port
        self.path = f"database/listeners/{self.name}/"
        self.isRunning  = False
        self.app = Flask(__name__)
        os.makedirs(self.path, exist_ok=True)

    def save(self):
        data = {
            'name': self.name,
            'type': "HTTP",
            'bind_address': self.bind_address,
            'bind_port': self.bind_port,
        }
        filename = os.path.join(self.path, f"{self.name}_listener.json")
        with open(filename, 'w') as f:
            json.dump(data, f)

def get_local_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip
def load_listeners():
    listeners = []

    # Load all listeners from the database directory
    listeners_directory = "database/listeners/"
    if os.path.exists(listeners_directory):
        for listener_name in os.listdir(listeners_directory):
            file_path = listeners_directory + listener_name + "/" + listener_name + "_listener.json"
            with open(file_path, 'r') as f:
                data = json.load(f)

            listener = Listener(**data)
            if listener.bind_address == get_local_ip():
                listener.isRunning = True
            if listener.isRunning:
                status = "Running"
            else:
                status = "Not running"

            listeners.append((listener.name,
                              listener.type,
                              status,
                              listener.bind_address,
                              listener.bind_port))
    return listeners

@listeners_bp.route('/', methods=['GET', 'POST'])
def listeners():
    listener_list = load_listeners()
    return render_template('listeners.html', listeners = listener_list)

@listeners_bp.route('/edit', methods=['GET', 'POST'])
def edit_listener():
    form = EditListener(request.form)
    if form.is_submitted():
        name = form.name.data
        type = form.type.data
        bind_address = form.bind_address.data
        bind_port = form.bind_port.data
        
        listener = Listener(name, type, bind_address, bind_port)
        listener.save()

        print('Edit listener successfully!')
        return redirect(url_for('listeners.listeners'))
    else:
        print('Edit fails!')
    return render_template('edit_listener.html', form = form)



