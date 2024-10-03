import requests
import os

class PDFDownloader:
    """
    The class downloads  PDF file from a specified URL and saves it to the current work directory.

    Attributes:
        url (str): The URL of the PDF file to be downloaded.
        save_directory (str): The directory where the PDF file will be saved. Defaults to the current working directory.
        pdf_filename (str): The name of the PDF file to be saved. Defaults to "GEM_Report.pdf".
        save_path (str): The full path where the PDF file will be saved, constructed from save_directory and pdf_filename.

    Methods:
        download_pdf():
            Downloads the PDF from the specified URL and saves it to the designated directory.
            Raises an exception if the download fails due to a network error or an invalid URL.
    """

    def __init__(self, url, save_directory=os.getcwd(), pdf_filename="GEM_Report.pdf"):
        self.url = url
        self.save_directory = save_directory
        self.pdf_filename = pdf_filename
        self.save_path = os.path.join(self.save_directory, self.pdf_filename)

    def download_pdf(self):
        try:
            
            response = requests.get(self.url)
            response.raise_for_status()  # Check if the request was successful

            # Write the PDF content to a file
            with open(self.save_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f"PDF successfully downloaded as: {self.pdf_filename}\n")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download PDF: {e}")

