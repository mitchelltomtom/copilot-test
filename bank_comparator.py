# Import necessary libraries
import os
import constants
from summarise_pdf import summarise_pdf

# Set the directory path where the PDFs are located
PDF_DIR = './test_data'
os.environ["OPENAI_API_KEY"] = constants.API_KEY


# Iterate through all the PDFs in the directory
for filename in os.listdir(PDF_DIR):
    if filename.endswith('.pdf'):
        # Apply the summarize_pdf function to the PDF
        pdf_path = os.path.join(PDF_DIR, filename)
        summary = summarise_pdf(pdf_path, constants.API_KEY, 'gpt-3.5-turbo')
        print(summary)
