# -*- coding: utf-8 -*-
import uuid
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from flask_mail import Message
from App.Models import Profile, User

def exciting_app_routes(app, db, mail):

    @app.route("/")
    def index():
        return render_template("index.html")

    @permission_required(resource="update", action="profile")
    def things():
        return render_template("things.html")
    app.add_url_rule("/things", "things", things)
