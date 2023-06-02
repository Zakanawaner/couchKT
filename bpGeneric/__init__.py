from flask import Blueprint, render_template, current_app
from flask_login import current_user

from utils.package import getAllPackages


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def generalEndPoint():
    return render_template(
        'general.html',
        title=current_app.config['WEB_NAME'] + " - " + "General",
        packages=getAllPackages(),
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/about", methods={"GET", "POST"})
def aboutEndPoint():
    return render_template(
        'about.html',
        title=current_app.config['WEB_NAME'] + " - " + "About",
        packages=getAllPackages(),
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/contact", methods={"GET", "POST"})
def contactEndPoint():
    return render_template(
        'contact.html',
        title=current_app.config['WEB_NAME'] + " - " + "Contact",
        packages=getAllPackages(),
        user=current_user if not current_user.is_anonymous else None
    )