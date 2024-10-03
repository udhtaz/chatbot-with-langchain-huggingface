from flask import Blueprint
from flask_restx import Api
from app.api.resources_llmchat import llmchat_ns
from app.api.resources_health import health_ns


api_bp = Blueprint('api', __name__, url_prefix='/api')
api_restx = Api(api_bp, doc='/doc', title='RAG Open Source LLM', 
          version='1.0', description='RAG API Documentation')

for rag_api_namespace in [health_ns, llmchat_ns]:
    api_restx.add_namespace(rag_api_namespace)
