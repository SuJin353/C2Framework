from flask import Blueprint, render_template, redirect, request, url_for
import flask
import os
import json
agents_bp = Blueprint('agents', __name__, template_folder='templates', static_folder='static')


class Agent:

    def __init__(self, name, listener, type, remote_address, hostname):

        self.name = name
        self.listener = listener
        self.type = type
        self.remote_address = remote_address
        self.hostname = hostname
        self.sleep = 3
        self.path = f"database/agents"
        os.makedirs(self.path, exist_ok=True)

    def save(self):
        data = {
            'name': self.name,
            'listener': self.listener,
            'type': self.type,
            'remote_address': self.remote_address,
            'hostname': self.hostname,
        }
        filename = os.path.join(self.path, f"{self.name}_agent.json")
        with open(filename, 'w') as f:
            json.dump(data, f)

@agents_bp.route('/', methods=['GET','POST'])
def agents():
    if request.method == 'POST':
        hostname = flask.request.form.get("name")
        type = flask.request.form.get("type")
        remote_address = flask.request.form.get("remote_ip")
        print('agent checked in', remote_address, hostname, type)

        agent = Agent('agent1', 'test_2', type, remote_address, hostname)

        agent.save()
    else:
        agents = []

        agents_directory = "database/agents/"
        if os.path.exists(agents_directory):
            for agent_name in os.listdir(agents_directory):
                file_path = os.path.join(agents_directory, agent_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)

                agent = Agent(**data)

                agents.append((agent.name,
                                  agent.listener,
                                  agent.type,
                                  agent.remote_address,
                                  agent.hostname))

    return render_template('agents.html', agents = agents)






