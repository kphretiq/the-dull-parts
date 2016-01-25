# -*- coding: utf-8 -*-
import uuid
import sqlalchemy
from flask import Flask, render_template, abort, request, session, redirect, url_for
from flaskext.auth import permission_required
from flask_mail import Message
from App.Models import *

def palimpsest_media_routes(app, db):

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
            try:
                media = Media(
                        name = request.form["name"],
                        uri = request.form["uri"],
                        mime_type = request.form["mime_type"],
                        alt = request.form["alt"],
                        page_id = data.id,
                        )
                db.session.add(media)
                db.session.commit()
            except Exception as error:
                return render_template("error.html", error=error)
            return redirect("/p/update/%s"%name)
        return render_template("palimpsest/media/create.html", data=data)

        return render_template("palimpsest/media/create.html", data=data)
    app.add_url_rule(
            "/p/update/media/<string:name>",
            "update_media",
            update,
            methods=["GET", "POST"],
            )

    @permission_required(resource="create", action="flow")
    def delete(media_id):
        return "nothing"
    app.add_url_rule(
            "/p/delete/media/<int:media_id>",
            "delete_media",
            delete,
            methods=["GET", "POST"],
            )
