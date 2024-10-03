from flask_restx import Resource, Namespace, reqparse
import datetime
import requests
from flask import request

import logging
logging.basicConfig(level = logging.INFO)

health_ns = Namespace('health', description='APP Health related operations')

SERVER_ERROR = "error starting server"


@health_ns.route('/health_check', methods=['GET'])
class health_check(Resource):
    def get(self):

        """Confirms the service is running"""

        try:
            notification = {"Health Check" : "Server is up and running..."}
        except Exception as err:
            logging.info(f"Error starting server: {err}")
            notification = {SERVER_ERROR}

        return notification
