import json
import secrets
import os

from flask_mail import Mail

from database import db, User, Package
from bpAuth import loginManager, jwt


def createApp(app):
    config = json.load(open("secret/config.json"))

    app.config["SECRET_KEY"] = handleSecretKey()
    app.config['PORT'] = config['port']
    app.config['HOST'] = config['host']

    app.config["JWT_SECRET_KEY"] = handleSecretKey()
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    app.config["SQLALCHEMY_DATABASE_URI"] = config['db-uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["ADMIN_USERNAME"] = config['admin-name']
    app.config["ADMIN_PASSWORD"] = config['admin-password']

    app.config["COLLABORATOR_USERNAME"] = config['coach-name']
    app.config["COLLABORATOR_PASSWORD"] = config['coach-password']

    app.config["WEB_NAME"] = config['web-name']
    app.config["PACKAGES"] = config['packages']

    app.config["MAIL_SERVER"] = config['mail-server']
    app.config["MAIL_PORT"] = config['mail-port']
    app.config["MAIL_USE_TLS"] = config['mail-use-tls']
    app.config["MAIL_USE_SSL"] = config['mail-use-ssl']
    app.config["MAIL_USERNAME"] = config['mail-username']
    app.config["MAIL_PASSWORD"] = config['mail-password']

    loginManager.init_app(app)
    app.config["loginManager"] = loginManager
    jwt.init_app(app)
    app.config["jwt"] = jwt
    db.init_app(app)
    app.config["database"] = db
    mail = Mail()
    mail.init_app(app)
    app.config["mail"] = mail

    return app


def createDatabase(app):
    with app.app_context():
        if os.path.exists('database.txt'):
            pass
        else:
            createTables(app.config['database'])
            createAdmin(app)
            createCollaborator(app)
            createPackages(app)
            file = open('database.txt', 'w')
            file.write("Database Created")
            file.close()


def handleSecretKey():
    keys = json.load(open("secret/config.json"))
    if keys['secret-key']:
        return keys['secret-key']
    else:
        key = secrets.token_hex(16)
        keys['secret-key'] = key
        json.dump(keys, open("secret/config.json", 'w'), indent=4)
        return key


def createTables(database):
    database.create_all()
    database.session.commit()


def createAdmin(app):
    if User.query.filter_by(name=app.config["ADMIN_USERNAME"]).first():
        return
    new_user = User(
        name=app.config["ADMIN_USERNAME"],
        password=app.config["ADMIN_PASSWORD"],
        permissions=15
    )
    app.config['database'].session.add(new_user)
    app.config['database'].session.commit()


def createCollaborator(app):
    if User.query.filter_by(name=app.config["COLLABORATOR_USERNAME"]).first():
        return
    new_user = User(
        name=app.config["COLLABORATOR_USERNAME"],
        password=app.config["COLLABORATOR_PASSWORD"],
        permissions=13
    )
    app.config['database'].session.add(new_user)
    app.config['database'].session.commit()


def createPackages(app):
    for pkg in app.config["PACKAGES"]:
        if not Package.query.filter_by(title=pkg["name"]).first():
            new_pkg = Package(
                title=pkg["name"],
                shortName=pkg['name'].lower().replace(" ", ""),
                description=pkg['description'],
                price=float(pkg['price'])
            )
            app.config['database'].session.add(new_pkg)
    app.config['database'].session.commit()
