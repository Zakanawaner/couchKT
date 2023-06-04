import datetime

from database import Blog


def addBlog(form, database):
    if Blog.query.filter_by(title=form['title']).first():
        return 402, None
    blog = Blog(
        title=form["title"] if "title" in form.keys() else "Title",
        shortName=form["title"].lower().replace(" ", "") if "title" in form.keys() else "title",
        description=form["description"] if "description" in form.keys() else "Description",
        url=form["url"] if "url" in form.keys() else "",
        date=datetime.datetime.today(),
    )
    database.session.add(blog)
    database.session.commit()


def deleteBlog(form, database):
    database.session.delete(Blog.query.filter_by(shortName=form['entry']).first())
    database.session.commit()
    return 200


def getBlog(shortName):
    return Blog.query.filter_by(shortName=shortName).first()


def getAllBlogs():
    return Blog.query.all()
