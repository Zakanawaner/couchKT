import os

from flask import Blueprint, redirect, url_for, current_app, request, flash, render_template
from flask_login import login_required, current_user

from utils.user import setPlayerPermission, getUserOnly
from utils.package import addPackage, deletePackage, getAllPackages
from utils.blog import addBlog, getAllBlogs, deleteBlog
from utils.decorators import only_admin


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
        permissions=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])


@adminBP.route("/blog/add", methods={"GET", "POST"})
@login_required
@only_admin
def addBlogEntryEndPoint():
    if request.method == "POST":
        entry = addBlog(request.form, current_app.config['database'])
        return redirect(url_for('blogBluePrint.getBlogEndPoint', bl=entry.shortName))
    return render_template(
        'addBlogEntry.html',
        user=current_user if not current_user.is_anonymous else None)


@adminBP.route("/blog/delete", methods={"GET", "POST"})
@login_required
@only_admin
def deleteBlogEntryEndPoint():
    if request.method == "POST":
        deleteBlog(request.form, current_app.config['database'])
        return redirect(url_for('blogBluePrint.getAllBlogsEndPoint'))
    return render_template(
        'deleteBlogEntry.html',
        blogs=getAllBlogs(),
        user=current_user if not current_user.is_anonymous else None)


@adminBP.route("/package/add", methods={"GET", "POST"})
@login_required
@only_admin
def addPackageEndPoint():
    if request.method == "POST":
        addPackage(request.form, current_app.config['database'])
        return redirect(url_for('genericBluePrint.generalEndPoint'))
    return render_template(
        'addPackage.html',
        user=current_user if not current_user.is_anonymous else None)


@adminBP.route("/package/<pk>/delete", methods={"GET", "POST"})
@login_required
@only_admin
def deletePackageEndPoint(pk):
    pkgs = getAllPackages()
    return render_template(
        'packages.html',
        title=current_app.config['WEB_NAME'] + " - " + pkg.title,
        user=current_user if not current_user.is_anonymous else None
    )


@adminBP.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        os.system('bash command-pull-event.sh')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
