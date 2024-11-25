from flask import Blueprint, render_template, redirect, request, url_for
from .create_listener import CreateListener

import threading
import os
import json

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
        os.makedirs(self.path, exist_ok=True)

    def setFlag(self):
        self.flag = 1

    def saveListeners(self):
        data = {
            'name': self.name,
            'type': self.type,
            'bind_address': self.bind_address,
            'bind_port': self.bind_port,
        }

        filename = os.path.join(self.path, f"{self.name}_listener.json")
        with open(filename, 'w') as f:
            json.dump(data, f)
    @staticmethod
    def load(name):
        path = f"database/listeners/{name}/{name}_listener.json"
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                return Listener(**data)

@listeners_bp.route('/', methods=['GET', 'POST'])
def listeners():
    listeners = []

    # Load all listeners from the database directory
    listeners_directory = "database/listeners/"
    if os.path.exists(listeners_directory):
        for listener_name in os.listdir(listeners_directory):
            listener = Listener.load(listener_name)
            if listener:
                listeners.append((listener.name,
                                  listener.type,
                                  listener.isRunning,
                                  'dd//mm//yy',
                                  listener.bind_address,
                                  listener.bind_port))

    return render_template('listeners.html', listeners = listeners)

@listeners_bp.route('/create', methods=['GET', 'POST'])
def create_listener():
    form = CreateListener(request.form)
    if form.is_submitted():
        name = form.name.data
        type = form.type.data
        bind_address = form.bind_address.data
        bind_port = form.bind_port.data
        
        listener = Listener(name, type, bind_address, bind_port)
        listener.saveListeners()

        print('Listener created successfully!')
        return redirect(url_for('listeners.listeners'))
    else:
        print('Listener created fails!')
    return render_template('create_listener.html', form = form)



