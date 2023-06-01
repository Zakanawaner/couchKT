from database import Package


def addPackage(form, database):
    if Package.query.filter_by(name=form['name']).first():
        return 402, None

    new_pkg = Package(
        name=form['name'],
        shortName=form['name'].lower().replace(" ", ""),
        description=form['description'],
        price=float(form['price'])
    )
    database.session.add(new_pkg)
    database.session.commit()


def getPackage(shortName):
    return Package.query.filter_by(shortName=shortName).first()


def getAllPackages():
    return Package.query.all()
