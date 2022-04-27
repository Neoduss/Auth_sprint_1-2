import os
import uuid

from flask import Blueprint, jsonify, request
from flask_restx import Resource, reqparse

from src.app.api.v1.service.datastore.roles_datastore import RolesCRUD
from src.app.utils.pagination import get_paginated_list

roles = Blueprint('roles', __name__)

ROLE_START_PAGE = os.getenv('ROLE_START_PAGE')
ROLE_PAGE_LIMIT = os.getenv('ROLE_PAGE_LIMIT')


class RolesAPI(Resource):
    """
    Логика работы метода api/v1/roles
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=uuid.uuid4(), required=False, help="id")
    parser.add_argument('role', type=str, required=False, help="role")
    parser.add_argument('description', type=str, required=False, help="description")

    @staticmethod
    def get():
        return jsonify(get_paginated_list(RolesCRUD.get_all_roles(), '/api/v1/roles',
                                          start=request.args.get('start', ROLE_START_PAGE),
                                          limit=request.args.get('limit', ROLE_PAGE_LIMIT)))

    @staticmethod
    def post():
        body = request.get_json()
        try:
            return jsonify({'message': 'Role Created'},
                           RolesCRUD.create_role(body.get("role"), body.get("description")))
        except Exception as e:
            return str(e)

    @staticmethod
    def put():
        body = request.get_json()
        try:
            RolesCRUD.update_role(body.get("id"), body.get("role"), body.get("description"))
            return {'message': 'Role Updated'}
        except Exception as e:
            return str(e)

    @staticmethod
    def delete():
        body = request.get_json()
        try:
            RolesCRUD.delete_role(body.get("id"))
            return {'message': 'Role Deleted'}
        except Exception as e:
            return str(e)


class UserRolesAPI(Resource):
    """
        Логика работы метода api/v1/user-roles
        """

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=uuid.uuid4(), required=False, help="user_id")
    parser.add_argument('role_id', type=uuid.uuid4(), required=False, help="role_id")

    @staticmethod
    def get():
        body = request.get_json()
        return jsonify(RolesCRUD.check_user_role(body.get("user_id")))

    @staticmethod
    def post():
        body = request.get_json()
        try:
            jsonify(RolesCRUD.add_role_to_user(body.get("user_id"), body.get("role_id")))
            return {'message': 'Role added to User'}
        except Exception as e:
            return str(e)

    @staticmethod
    def delete():
        body = request.get_json()
        try:
            jsonify(RolesCRUD.delete_user_role(body.get("user_id"), body.get("role_id")))
            return {'message': 'User role deleted'}
        except Exception as e:
            return str(e)
