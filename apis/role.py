#!/usr/bin/env python
# encoding: utf-8
"""

 @license: Licensed Materials - Property of IBM

 @copyright: (c) Copyright IBM Corporation 2014, 2015. All Rights Reserved.

 @note: Note to U.S. Government Users Restricted Rights: Use, duplication or disclosure restricted by GSA ADP
 Schedule Contract with IBM Corp.

 @author: Sovongsa Ly

 @contact: sly@us.ibm.com
"""

import json
from flask import Flask, request
from flask_restplus import Namespace, Resource, fields, reqparse,abort

app = Flask(__name__)
ns = Namespace('Role', description='Role API Version 1.0')



# permission = ns.model('permission',{
#     "name":fields.String(required=True),
#     "resourcetype":fields.String(required=True),
#     "create":fields.Boolean(required=True),
#     "update":fields.Boolean(required=True),
#     "read":fields.Boolean(required=True),
#     "delete":fields.Boolean(required=False),
# })
#
# role_model = ns.model('role', {
#     "name": fields.String(required=True),
#     "scope": fields.String(required=True),
#     "permissions":fields.List(fields.Nested(permission),required=True),
#     "idprolemap":fields.List(fields.String,required=True)
#
# })


@ns.route('/v1/roles')
class RoleList(Resource):
    # @ns.expect(role_model)
    # def post(self):
    #   """
    #   post a new role
    #   """
    #   data = json.dumps(request.get_json())
    #   name = json.loads(data)['name']
    #   status, response = roleservice.createRole(name,data)
    #   if status == False:
    #       abort (400,response)
    #   return json.loads(response),200

    @ns.param('idprolemap', description="external role")
    def get(self):
        """
        get role list 
        get role list and can filter by idprolemap 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('idprolemap', type=str)
        args = parser.parse_args()
        # status,response = roleservice.getRoleList(args)
        # if status == False :
        #     abort(400,response)
        return args['idprolemap'],200
