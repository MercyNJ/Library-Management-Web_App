from flask import Flask
from user import user_bp, login_manager
from members import members_bp
from books import books_bp
from issuance import issuance_bp
from statement import statement_bp
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')

    app.register_blueprint(user_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(issuance_bp)
    app.register_blueprint(statement_bp)

    login_manager.init_app(app)

    app.config['LOGIN_DISABLED'] = False
    app.config['LOGIN_VIEW'] = 'user.login'
    app.config['REFRESH_VIEW'] = 'user.login'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
