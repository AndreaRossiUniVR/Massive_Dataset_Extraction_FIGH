import sys
import re
import os
import PyPDF2

if len(sys.argv) < 2:
    print("Usage: python read.py <pdf_file>")
    sys.exit(1)

# Get the input PDF file from the command-line argument
input_pdf_file = sys.argv[1]

try:
    # Open the PDF file in read binary mode
    pdf_file = open(input_pdf_file, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages in the PDF document
    num_pages = len(pdf_reader.pages)

    # Loop through each page in the PDF document
    for page in range(num_pages):
        # Get the text from this page
        page_text = pdf_reader.pages[page].extract_text()

        # Extract home and away team names from the text
        home_team_regex = re.compile(r'Data\d{1,2}/\d{1,2}/\d{4}\n(.+)\n')
        home_team_search = home_team_regex.search(page_text)
        home_team = home_team_search.group(1).strip() if home_team_search else "Not found"

        away_team_regex = re.compile(r'Uff\.E\n(.+)\n')
        away_team_search = away_team_regex.search(page_text)
        away_team = away_team_search.group(1).strip() if away_team_search else "Not found"

        # Remove "A" or "B" from the beginning of the team names
        home_team = home_team[1:].strip() if home_team.startswith("A") or home_team.startswith("B") else home_team
        away_team = away_team[1:].strip() if away_team.startswith("A") or away_team.startswith("B") else away_team

        # Print the team names
        print(f"Home Team: {home_team}")
        print(f"Away Team: {away_team}")

    # Check if home and away team names are empty or contain only spaces
    if not home_team.strip() or not away_team.strip():
        # Check if the Log folder exists, create it if not
        log_folder = "Log"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        # Open or create the teamscanerr.txt file
        with open(os.path.join(log_folder, "teamscanerr.txt"), "a") as error_file:
            # Determine the error message based on the team names
            if not home_team.strip() and not away_team.strip():
                error_message = f"home_away_{os.path.basename(input_pdf_file)}"
            elif not home_team.strip():
                error_message = f"home_{os.path.basename(input_pdf_file)}"
            else:
                error_message = f"away_{os.path.basename(input_pdf_file)}"

            # Write the error message as a new line in the file
            error_file.write(f"{error_message}\n")

    # Close the PDF file
    pdf_file.close()

except PyPDF2.utils.PdfReadError:
    print(f"Error: File {input_pdf_file} is not a valid PDF file.")

except PyPDF2.errors.EmptyFileError:
    print(f"Error: File {input_pdf_file} is empty.")
