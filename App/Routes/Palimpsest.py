# -*- coding: utf-8 -*-
import uuid
import sqlalchemy
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from flask_mail import Message
from App.Models import *

def palimpsest_routes(app, db):

    @app.route("/p/read/<string:name>")
    def read(name):
        try:
            data = Page.query.filter(Page.name == name).one()
        except sqlalchemy.orm.exc.NoResultFound:
            error = "This page does not exist." 
            return render_template("error.html", error=error)
        except Exception as error: 
            return render_template("error.html", error=error)
        return render_template("palimpsest/read.html", data=data)

    @permission_required(resource="create", action="flow")
    def create(name):
        return render_template("palimpsest/create.html")
    app.add_url_rule(
            "/p/create/<string:name>",
            "create_flow",
            create,
            methods=["GET", "POST"],
            )

    @permission_required(resource="create", action="flow")
    def delete(level, name):
        return render_template("palimpsest/delete.html")
    app.add_url_rule(
            "/p/delete/<string:level>/<string:name>",
            "delete_flow",
            delete,
            methods=["GET", "POST"],
            )

    @permission_required(resource="create", action="flow")
    def update(name):
        """
        add media
        add child
        move node (and thereby move children) by changing parent_id value
        """
        return render_template("palimpsest/update.html")
    app.add_url_rule(
            "/p/update/<string:name>",
            "update_flow",
            create,
            methods=["GET", "POST"],
            )

