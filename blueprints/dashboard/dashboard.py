from flask import Blueprint, render_template, redirect, request

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

@dashboard_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

