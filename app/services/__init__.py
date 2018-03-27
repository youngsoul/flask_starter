from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.services import auth_services
