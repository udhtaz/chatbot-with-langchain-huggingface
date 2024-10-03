import io
from flask_restx import Resource, Namespace
import requests

import logging
logging.basicConfig(level = logging.INFO)

from app.api_config import llmchat_input
from app.utils import generate_response


llmchat_ns = Namespace('llmchat', description='Chatbot related operations')
llmchat_input_schema = llmchat_ns.model('llmchat', llmchat_input)

LLM_NOT_FOUND = "Error generating response from query"


@llmchat_ns.route('/llm_chat_text')
class LLM_Chat_Text(Resource):   
    @llmchat_ns.expect(llmchat_input_schema)
    def post(self):
        query = llmchat_ns.payload['query']

        try:
            chat_response = generate_response(query)
        except Exception as err:
            logging.info(f"Error generating response: {err}")
            chat_response = {LLM_NOT_FOUND}
        # return {"response": generated_response}, 200
        return chat_response, 200
