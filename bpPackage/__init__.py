from flask import Blueprint, render_template, current_app
from flask_login import current_user

from utils.package import getPackage, getAllPackages, deletePackage


packageBP = Blueprint('packageBluePrint', __name__)


@packageBP.route("/packages", methods={"GET", "POST"})
def getAllPackagesEndPoint():
    return render_template(
        'packages.html',
        title=current_app.config['WEB_NAME'] + " - " + "Packages",
        packages=getAllPackages(),
        user=current_user if not current_user.is_anonymous else None
    )


@packageBP.route("/package/<pk>", methods={"GET", "POST"})
def packageEndPoint(pk):
    pkg = getPackage(pk)
    return render_template(
        'package.html',
        title=current_app.config['WEB_NAME'] + " - " + pkg.title,
        package=pkg,
        user=current_user if not current_user.is_anonymous else None
    )
