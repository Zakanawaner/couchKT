from flask import current_app
from sqlalchemy import desc

from werkzeug.security import generate_password_hash, check_password_hash

from database import *


def userSignup(database, form):
    if form['username'].isalnum():
        if form['password'] == form['password1']:
            hashed_password = generate_password_hash(form['password'], method='sha256')
            if User.query.filter_by(name=form['username']).first():
                return 402, None

            new_user = User(
                bcpId=bcpId,
                name=form['username'],
                password=hashed_password,
                bcpName=user["data"][0]['user']['firstName'] + " " + user["data"][0]['user']['lastName'],
                shortName=form['username'].lower().replace(" ", ""),
                permissions=0
            )
            database.session.add(new_user)
            database.session.commit()
            return 200, new_user
    return 405, None


def userLogin(form):
    if form['username'].isalnum():
        user = User.query.filter_by(name=form['username']).first()
        if user:
            if check_password_hash(user.password, form['password']):
                return 200, user
    return 401, None


def setPlayerPermission(database, userId, form):
    try:
        lvl = form['permission']
        usr = User.query.filter_by(id=userId).first()
        usr.permissions = int(lvl)
        database.session.commit()
    except:
        return False
    return True


def getUser(pl):
    return current_app.config["database"].session.query(UserTournament, User, Tournament
                                                        ).order_by(desc(UserTournament.bcpScore)).filter(UserTournament.userId == pl
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(User,
                                                                               User.id == UserTournament.userId).all()


def getUserBestTournaments(pl):
    return UserTournament.query.filter_by(userId=int(pl)).order_by(desc(UserTournament.bcpScore)).limit(4).all()


def getUserOnly(pl):
    return User.query.filter_by(id=pl).first()


def getUsers(country, qty=0):
    if qty > 0:
        result = User.query.filter(User.bcpId != "0000000000").filter(User.bcpScore > 0).order_by(desc(User.bcpScore)).all() if country == "latam" else User.query.filter(User.bcpId != "0000000000").filter_by(country=current_app.config["COUNTRIES"][country]).order_by(desc(User.bcpScore)).all()
        return result[0:qty-1]
    else:
        return User.query.filter(User.bcpId != "0000000000").filter(User.bcpScore > 0).order_by(desc(User.bcpScore)).all() if country == "latam" else User.query.filter(User.bcpId != "0000000000").filter_by(country=current_app.config["COUNTRIES"][country]).order_by(desc(User.bcpScore)).all()


def addUser(db, usr, tor):
    if not User.query.filter_by(bcpId=usr['userId']).first():
        db.session.add(User(
            bcpId=usr['userId'],
            bcpName=usr['user']['firstName'].strip() + " " + usr['user']['lastName'].strip(),
            country=tor.country,
            permissions=0
        ))
    db.session.commit()
    return User.query.filter_by(bcpId=usr['userId']).first()
