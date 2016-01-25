# -*- coding: utf-8 -*-
import time
import os
import base64
import hmac
import urllib
from hashlib import sha1
from flask.ext import restful
from flask_restful import reqparse

def media(app):

    api = restful.Api(app)

    class GetSignedRequest(restful.Resource):
        """
        create a signed request for xhr
        """
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument(
                    "filepath", type=str, help="path of file to upload"
                    )
            parser.add_argument(
                    "mimetype", type=str, help="mimetype of file"
                    )
            args = parser.parse_args()
            filename = args["filepath"].split("\\").pop()
            mime_type = args["mimetype"]
            object_name = urllib.quote_plus(filename)
            expires = int(time.time()+60*60*24)
            amz_headers = "x-amz-acl:public-read"
            string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (
                    args["mimetype"],
                    expires,
                    amz_headers,
                    app.config["AWS_STORAGE_BUCKET_NAME"],
                    object_name,
                    )
            signature = base64.encodestring(
                    hmac.new(
                        app.config["AWS_SECRET_ACCESS_KEY"].encode(),
                        string_to_sign.encode('utf8'),
                        sha1,
                        ).digest()
                    )
            signature = urllib.quote_plus(signature.strip())
            url = "https://%s.s3.amazonaws.com/%s"%(
                    app.config["AWS_STORAGE_BUCKET_NAME"],
                    object_name,
                    )
            signed_request = '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s'%(
                    url,
                    app.config["AWS_ACCESS_KEY_ID"],
                    expires,
                    signature,
                    )
            return {
                'signed_request': signed_request,
                'url': url,
                }

    api.add_resource(GetSignedRequest, "/api/media/request")

    #TODO I suggest you take a look at zipapottam.us.
