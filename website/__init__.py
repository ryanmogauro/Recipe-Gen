"""Website init file"""
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Create app"""
    app = Flask(__name__)

    if os.environ.get('CONFIG_TYPE') == 'config.TestingConfig':
        app.config['SECRET_KEY'] = 'secret'
    else:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') # pragma: no cover

    from website.views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':  # pragma: no cover
    my_app = create_app()
    my_app.run(debug=True)  # pragma: no cover
