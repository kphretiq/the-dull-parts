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
        # front page!
        if data.id == 1:
            return render_template("palimpsest/front.html", data=data)
        return render_template("palimpsest/read.html", data=data)

    @permission_required(resource="create", action="flow")
    def create(parent_id):
        if request.method == "POST":
            for k in ["name", "blurb", "content"]:
                if not k in request.form:
                    error = "% value is required!"%k
                    return render_template("error.html", error=error)
            data = Page(
                    parent_id = parent_id,
                    name = request.form["name"],
                    blurb = request.form["blurb"],
                    content = request.form["content"],
                    )
            db.session.add(data)
            db.session.commit()
            return redirect("/p/update/%s"%request.form["name"])

        return render_template("palimpsest/create.html")
    app.add_url_rule(
            "/p/create/<int:parent_id>",
            "create_flow",
            create,
            methods=["GET", "POST"],
            )

    @permission_required(resource="create", action="flow")
    def delete(name):
        return render_template("palimpsest/delete.html")
    app.add_url_rule(
            "/p/delete/<string:level>/<string:name>",
            "delete_flow",
            delete,
            methods=["GET", "POST"],
            )

    @permission_required(resource="create", action="flow")
    def update(name):
        """{% if not child.id==1 %}

        add media
        add child
        move node (and thereby move children) by changing parent_id value
        """
        try:
            data = Page.query.filter(Page.name == name).one()
        except Exception as error:
            return render_template("error.html", error=error)

        if request.method == "POST":
            for k in ["name", "blurb", "content"]:
                if not k in request.form:
                    error = "% value is required!"%k
                    return render_template("error.html", error=error)
                else:
                    print k, request.form[k]
                    setattr(data, k, request.form[k])

            if "role" in request.form:
                setattr(data, "role", request.form["role"])

            db.session.add(data)
            db.session.commit()

            print(request.form.keys())

        return render_template("palimpsest/create.html", data=data)
    app.add_url_rule(
            "/p/update/<string:name>",
            "update_flow",
            update,
            methods=["GET", "POST"],
            )
