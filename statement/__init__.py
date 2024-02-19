from flask import Blueprint

statement_bp = Blueprint('statement', __name__)

from . import statement_views
