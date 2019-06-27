from flask import Flask
from flask_jwt_extended import JWTManager

from main.controllers.category import bp_category
from main.controllers.item import bp_item
from main.controllers.user import bp_user, bp_auth
from main.utils.exception import UnauthorizedError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://namtran166:123456@@127.0.0.1/gotit"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'brian'
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.expired_token_loader
def expired_token_handler():
    raise UnauthorizedError("Access token has expired.")


app.register_blueprint(bp_category)
app.register_blueprint(bp_item)
app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)

if __name__ == '__main__':
    from main.database import db

    db.init_app(app)
    app.run(port=5000, debug=True)
