import sys
import re
import os
import PyPDF2
import sqlite3

if len(sys.argv) < 2:
    print("Usage: python read.py <pdf_file>")
    sys.exit(1)

input_pdf_file = sys.argv[1]
pdf_file = open(input_pdf_file, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

num_pages = len(pdf_reader.pages)

game = [[""] * 5 for _ in range(3)]
game[0][0] = input_pdf_file
game_number = re.findall(r'\d+', input_pdf_file)
game[0][1] = game_number[0] if game_number else "Not found"

# Extract date 
date_regex = re.compile(r'Data(\d{2}/\d{2}/\d{4})\nA')
for page in range(num_pages):
    page_text = pdf_reader.pages[page].extract_text()
    date_search = date_regex.search(page_text)
    if date_search:
        game[0][2] = date_search.group(1).strip()
        break

category_regex = re.compile(r'GIUOCO HANDBALL\s*(.*?)\s*Numero', re.DOTALL)
for page in range(num_pages):
    page_text = pdf_reader.pages[page].extract_text()
    category_search = category_regex.search(page_text)
    if category_search:
        game[0][3] = category_search.group(1).strip()
        break

for page in range(num_pages):
    page_text = pdf_reader.pages[page].extract_text()

    home_team_regex = re.compile(r'Data\d{1,2}/\d{1,2}/\d{4}\n(.+)\n')
    home_team_search = home_team_regex.search(page_text)
    home_team = home_team_search.group(1).strip() if home_team_search else "Not found"
    home_team = home_team[1:] if home_team.startswith('A') or home_team.startswith('B') else home_team

    away_team_regex = re.compile(r'Uff\.E\n(.+)\n')
    away_team_search = away_team_regex.search(page_text)
    away_team = away_team_search.group(1).strip() if away_team_search else "Not found"
    away_team = away_team[1:] if away_team.startswith('A') or away_team.startswith('B') else away_team

    result_regex = re.compile(r'Risultato\sfinale\s(\d+)\s-\s(\d+)')
    result_search = result_regex.search(page_text)
    result = result_search.groups() if result_search else ("Not found", "Not found")
    home_goals = int(result[0])
    away_goals = int(result[1])

    home_team_players = 'A' + home_team
    away_team_players = 'B' + away_team

    players_regex = re.compile(r'(\d{1,2}[A-Za-z, ().]+,\s[A-Za-z\s]+\d+)')
    for page in range(num_pages):
        page_text = pdf_reader.pages[page].extract_text()

        page_text = '\n'.join(page_text.split('\n')[4:])

        home_players_start = page_text.find(home_team_players)
        away_players_start = page_text.find(away_team_players)

        home_players_text = page_text[home_players_start:away_players_start]
        away_players_text = page_text[away_players_start:]

        home_players = players_regex.findall(home_players_text)
        away_players = players_regex.findall(away_players_text)

    home_players = [{'number': re.split(r'(\d+)([^\d]+)(\d+)', player)[1],
                 'name': re.split(r'(\d+)([^\d]+)(\d+)', player)[2].strip(),
                 'goals': re.split(r'(\d+)([^\d]+)(\d+)', player)[3]} for player in home_players if 'Pagina' not in player]
    away_players = [{'number': re.split(r'(\d+)([^\d]+)(\d+)', player)[1],
                 'name': re.split(r'(\d+)([^\d]+)(\d+)', player)[2].strip(),
                 'goals': re.split(r'(\d+)([^\d]+)(\d+)', player)[3]} for player in away_players if 'Pagina' not in player]

    game[1][0] = home_team
    game[2][0] = away_team
    game[1][1] = home_goals
    game[2][1] = away_goals
    game[1][2] = away_goals
    game[2][2] = home_goals
    game[1][3] = home_players
    game[2][3] = away_players

db_conn = sqlite3.connect('fighDB.db')
c = db_conn.cursor()

# Insert the game into the Games table
c.execute('''
    INSERT INTO Games (id, home_team_id, away_team_id, home_goals, away_goals, category, date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (game[0][1], game[1][0], game[2][0], game[1][1], game[2][1], game[0][3], game[0][2]))

# Get the id of the game we just inserted
game_id = c.lastrowid

# Iterate over both teams
for team_index in [1, 2]:
    team_id = game[team_index][0] + game[0][3]
    team_id = team_id.replace(' ', '')

    # Insert into Teams with ON CONFLICT DO UPDATE
    c.execute('''
        INSERT INTO Teams (id, team_name, goals, goals_against, category)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET goals = goals + ?, goals_against = goals_against + ?
    ''', (team_id, game[team_index][0], game[team_index][1], game[team_index][2], game[0][3], game[team_index][1], game[team_index][2]))

    for player in game[team_index][3]:
        player_id = (player['number'] + game[team_index][0] + game[0][3]).replace(' ', '')

        c.execute('''
            INSERT INTO Players (id, team_id, game_id, number, name, goals)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_id, team_id, game_id, player['number'], player['name'], player['goals']))

db_conn.commit()
print('commit')

db_conn.close()

if any(not team[0].strip() for team in game[1:]):
    log_folder = "Log"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    with open(os.path.join(log_folder, "teamscanerr.txt"), "a") as error_file:
        for team in game[1:]:
            if not team[0].strip():
                error_message = f"{team[0]}_{os.path.basename(input_pdf_file)}"
                error_file.write(f"{error_message}\n")

pdf_file.close()

print(game)
