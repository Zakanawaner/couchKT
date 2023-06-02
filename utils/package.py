from database import Package


def addPackage(form, database):
    if Package.query.filter_by(title=form['title']).first():
        return 402, None
    new_pkg = Package(
        title=form["title"] if "title" in form.keys() else "Title",
        shortName=form["title"].lower().replace(" ", "") if "title" in form.keys() else "title",
        description=form["description"] if "description" in form.keys() else "Description",
        price=form["price"] if "price" in form.keys() else "price",
        promotion=form["isPromotion"],
        date=form["date"],
    )
    database.session.add(new_pkg)
    database.session.commit()


def deletePackage(form, database):
    database.session.delete(Package.query.filter_by(title=form['title']).first())
    database.session.commit()
    return 200


def getPackage(shortName):
    return Package.query.filter_by(shortName=shortName).first()


def getAllPackages():
    return Package.query.all()
