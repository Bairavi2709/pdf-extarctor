

import re
from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)


# Function to extract text and clean it
def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""

        # Extract text from each page
        for page in reader.pages:
            text += page.extract_text()

    # Filter the text to keep only alphanumeric characters and spaces
    filtered_text = ''.join(re.findall(r'[A-Za-z0-9\s]', text))

    return filtered_text


@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ""

    if request.method == 'POST':
        # Get the uploaded PDF file
        pdf_file = request.files['pdf_file']

        # Save the file to a local folder
        pdf_path = 'uploads/' + pdf_file.filename
        pdf_file.save(pdf_path)

        # Extract and filter the text from the PDF
        extracted_text = extract_text_from_pdf(pdf_path)

    return render_template('index.html', extracted_text=extracted_text)


if __name__ == "__main__":
    app.run(debug=True)

