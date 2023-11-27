from PyPDF2 import PdfReader
import re

# File path to the PDF
file_path = 'wvs_data/F00010738-WVS-7_Master_Questionnaire_2017-2020_English.pdf'  # Replace with your actual file path

# Function to read and extract text from a PDF file
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract questions following the pattern "Q<number>"
def extract_questions_with_q_prefix(text):
    question_pattern = re.compile(r'\bQ(\d+)\.?\s+([^\n]+)')
    return question_pattern.findall(text)

# Read the PDF file
pdf_text = read_pdf(file_path)

# Extract questions
questions = extract_questions_with_q_prefix(pdf_text)

def remove_trailing_numbers(text):
    return re.sub(r'\s*\d+(\s+\d+)*\s*$', '', text)
cleaned_questions = [(i,remove_trailing_numbers(q)) for i,q in questions]

# Output the extracted questions (or a sample of them)
print(questions[:10])
print(cleaned_questions[:10])  