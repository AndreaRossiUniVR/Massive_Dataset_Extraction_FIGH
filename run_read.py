import os
import subprocess

# Folder containing the PDF files
pdf_folder = "Dataset_FIGH"

# Iterate through all files in the folder
for file in os.listdir(pdf_folder):
    # Check if the file is a PDF file
    if file.lower().endswith(".pdf"):
        # Construct the file path
        file_path = os.path.join(pdf_folder, file)
        
        # Call the read.py script with the PDF file as an argument
        subprocess.run(["python", "read.py", file_path])
