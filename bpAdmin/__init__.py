import os

from flask import Blueprint, redirect, url_for, current_app, request, flash, render_template
from flask_login import login_required, current_user

from utils.user import setPlayerPermission, getUserOnly
from utils.package import getAllPackages
from utils.decorators import only_left_hand, only_collaborator, only_admin

adminBP = Blueprint('adminBluePrint', __name__)


@adminBP.route("/user/<us>/permission", methods={"GET", "POST"})
@login_required
@only_admin
def changePlayerPermissionsEndPoint(us):
    if request.method == "POST":
        if setPlayerPermission(current_app.config["database"], us, request.form):
            flash("OK")
        else:
            flash("No OK")
        return redirect(url_for('userBluePrint.userEndPoint', us=us))
    usr = getUserOnly(us)
    return render_template(
        'permissions.html',
        usr=usr,
        packages=getAllPackages(),
        permissions=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])


@adminBP.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system('bash command-pull-event.sh')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

