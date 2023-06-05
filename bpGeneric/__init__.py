from flask import Blueprint, render_template, current_app, request, flash
from flask_login import current_user
from flask_mail import Message


from utils.package import getAllPackages


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def generalEndPoint():
    return render_template(
        'general.html',
        title=current_app.config['WEB_NAME'] + " - " + "General",
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/about", methods={"GET", "POST"})
def aboutEndPoint():
    return render_template(
        'about.html',
        title=current_app.config['WEB_NAME'] + " - " + "About",
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/contact", methods={"GET", "POST"})
def contactEndPoint():
    if request.method == 'POST':
        email_subject = "Kill Team Academy - New message - " + request.form['name'] if 'name' in request.form.keys() else "Anonymous"
        email_message = request.form['message'] if 'message' in request.form.keys() else "Empty"
        email_client = request.form['email'] if 'email' in request.form.keys() else "No Email"
        email_package = request.form['packages'] if 'packages' in request.form.keys() else "No Package"
        msg = Message(
            email_subject,
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[current_app.config["MAIL_USERNAME"]]
        )
        msg.body = email_client + '\n\n' + 'Package selected: ' + email_package + '\n\n' + email_message
        current_app.config['mail'].send(msg)
        flash('Email Sent!')
    return render_template(
        'contact.html',
        title=current_app.config['WEB_NAME'] + " - " + "Contact",
        packages=getAllPackages(),
        user=current_user if not current_user.is_anonymous else None
    )
