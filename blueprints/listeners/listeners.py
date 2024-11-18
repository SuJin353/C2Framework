from flask import Blueprint, render_template, redirect, request

listeners_bp = Blueprint('listeners', __name__, template_folder='templates', static_folder='static')

@listeners_bp.route('/')
def listeners():
    return render_template('listeners.html')

@listeners_bp.route('/create')
def create_listener():
    return render_template('create_listener.html')

