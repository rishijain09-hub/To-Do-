from flask import Flask
import os
from models.tasks import init_db
from routes.main import main

app = Flask(__name__)

app.register_blueprint(main)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

