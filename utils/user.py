from database import *


def userLogin(form):
    if form['username'].isalnum():
        user = User.query.filter_by(name=form['username']).first()
        if user:
            if user.password == form['password']:
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


def getUserOnly(pl):
    return User.query.filter_by(id=pl).first()
