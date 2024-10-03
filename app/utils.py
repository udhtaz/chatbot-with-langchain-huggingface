#IMPORTS
from flask import current_app
import os
from urllib.parse import urlparse
import requests
import pandas as pd


from app.WorldBank_API import WorldBankDataAPI
from app.GEM_API import PDFDownloader
from app.LLM_API import cbfs


def get_worldbank_data():

    data_fetcher = WorldBankDataAPI()
    return data_fetcher.save_to_csv()


def get_gem_pdf(pdf_url):

    pdf_downloader = PDFDownloader(pdf_url)
    return pdf_downloader.download_pdf()


def generate_response(query):
    chatbot = cbfs()
    response = chatbot.ask_question(query)
    return response