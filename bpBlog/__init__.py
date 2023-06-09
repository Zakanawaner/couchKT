from flask import Blueprint, render_template, current_app
from flask_login import current_user

from utils.blog import getBlog, getAllBlogs


blogBP = Blueprint('blogBluePrint', __name__)


@blogBP.route("/blog", methods={"GET", "POST"})
def getAllBlogsEndPoint():
    return render_template(
        'blogs.html',
        title=current_app.config['WEB_NAME'] + " - " + "Blog",
        blogs=getAllBlogs(),
        user=current_user if not current_user.is_anonymous else None
    )


@blogBP.route("/blog/<bl>", methods={"GET", "POST"})
def getBlogEndPoint(bl):
    blg = getBlog(bl)
    return render_template(
        'blog.html',
        title=current_app.config['WEB_NAME'] + " - " + blg.title,
        blog=blg,
        user=current_user if not current_user.is_anonymous else None
    )
