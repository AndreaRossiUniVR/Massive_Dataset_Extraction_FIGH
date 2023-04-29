import sys
import re
import os
import PyPDF2

if len(sys.argv) < 2:
    print("Usage: python read.py <pdf_file>")
    sys.exit(1)

# Get the input PDF file from the command-line argument
input_pdf_file = sys.argv[1]

# Open the PDF file in read binary mode
pdf_file = open(input_pdf_file, 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Get the number of pages in the PDF document
num_pages = len(pdf_reader.pages)

# Initialize the list to store game information
game = [[""] * 4 for _ in range(3)]
game[0][0] = input_pdf_file

# Loop through each page in the PDF document
for page in range(num_pages):
    # Get the text from this page
    page_text = pdf_reader.pages[page].extract_text()

    # Extract home and away team names from the text
    home_team_regex = re.compile(r'Data\d{1,2}/\d{1,2}/\d{4}\n(.+)\n')
    home_team_search = home_team_regex.search(page_text)
    home_team = home_team_search.group(1).strip() if home_team_search else "Not found"
    home_team = home_team[1:] if home_team.startswith('A') or home_team.startswith('B') else home_team

    away_team_regex = re.compile(r'Uff\.E\n(.+)\n')
    away_team_search = away_team_regex.search(page_text)
    away_team = away_team_search.group(1).strip() if away_team_search else "Not found"
    away_team = away_team[1:] if away_team.startswith('A') or away_team.startswith('B') else away_team

    # Extract the final result from the text
    result_regex = re.compile(r'Risultato\sfinale\s(\d+)\s-\s(\d+)')
    result_search = result_regex.search(page_text)
    result = result_search.groups() if result_search else ("Not found", "Not found")
    home_goals = int(result[0])
    away_goals = int(result[1])

    # Store the extracted information in the game data structure
    game[1][0] = home_team
    game[2][0] = away_team
    game[1][1] = home_goals
    game[2][1] = away_goals
    game[1][2] = away_goals
    game[2][2] = home_goals
    game[1][3] = []  # Home team list of players
    game[2][3] = []  # Away team list of players

    # Print the team names and final result
    print(f"Home Team: {home_team}")
    print(f"Away Team: {away_team}")
    print(f"Final Result: {home_goals} - {away_goals}")

# Check if home and away team names are empty or contain only spaces
if any(not team[0].strip() for team in game[1:]):
    # Check if the Log folder exists, create it if not
    log_folder = "Log"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Open or create the teamscanerr.txt file
    with open(os.path.join(log_folder, "teamscanerr.txt"), "a") as error_file:
        # Determine the error message based on the team names
        for team in game[1:]:
                        if not team[0].strip():
                          error_message = f"{team[0]}_{os.path.basename(input_pdf_file)}"
                          # Write the error message as a new line in the file
                          error_file.write(f"{error_message}\n")

# Close the PDF file
pdf_file.close()

# Print the game data structure
for i in range(len(game)):
    for j in range(len(game[i])):
        print(f"game[{i}][{j}]: {game[i][j]}")

