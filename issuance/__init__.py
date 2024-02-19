from flask import Blueprint

issuance_bp = Blueprint('issuance', __name__)


from . import issuance_views
