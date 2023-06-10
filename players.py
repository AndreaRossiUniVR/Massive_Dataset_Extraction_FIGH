import sqlite3
import ipywidgets as widgets
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('fighDB.db')
c = conn.cursor()

# Get all unique categories
c.execute("SELECT DISTINCT category FROM Teams")
categories = [category[0] for category in c.fetchall()]

# Create the category dropdown menu
category_dropdown = widgets.Dropdown(options=categories, description='Category:')
display(category_dropdown)

# Create the team dropdown menu (empty for now)
team_dropdown = widgets.Dropdown(description='Team:')
display(team_dropdown)

# Create the player dropdown menu (empty for now)
player_dropdown = widgets.Dropdown(description='Player:')
display(player_dropdown)

# Create a button to confirm the category selection
category_button = widgets.Button(description="Confirm Category")
display(category_button)

# Function to update the team dropdown menu once a category is selected and confirmed
def update_teams(button):
    c.execute("SELECT team_name FROM Teams WHERE category=?", (category_dropdown.value,))
    teams = [team[0] for team in c.fetchall()]
    team_dropdown.options = teams

# Set the function to be called when the category button is clicked
category_button.on_click(update_teams)

# Create a button to confirm the team selection
team_button = widgets.Button(description="Confirm Team")
display(team_button)

# Function to update the player dropdown menu once a team is selected and confirmed
def update_players(button):
    team_id = (team_dropdown.value + category_dropdown.value).replace(" ", "")
    c.execute("SELECT name FROM Players WHERE team_id=?", (team_id,))
    players = [player[0] for player in c.fetchall()]
    player_dropdown.options = players

# Set the function to be called when the team button is clicked
team_button.on_click(update_players)

# Function to display the player stats
def display_player_stats(button):
    team_id = (team_dropdown.value + category_dropdown.value).replace(" ", "")
    player_name = player_dropdown.value

    c.execute('''
        SELECT game_id, goals
        FROM Players
        WHERE team_id=? AND name=?
    ''', (team_id, player_name))
    goals_per_game = c.fetchall()

    c.execute('''
        SELECT p.game_id, p.goals
        FROM Players p
        INNER JOIN Games g ON p.game_id = g.id
        WHERE p.team_id=? AND p.name=? AND ((g.home_team_id=? AND g.home_goals > g.away_goals) OR (g.away_team_id=? AND g.away_goals > g.home_goals))
    ''', (team_id, player_name, team_dropdown.value, team_dropdown.value))
    goals_per_game_wins = c.fetchall()

    c.execute('''
        SELECT p.game_id, p.goals
        FROM Players p
        INNER JOIN Games g ON p.game_id = g.id
        WHERE p.team_id=? AND p.name=? AND ((g.home_team_id=? AND g.home_goals < g.away_goals) OR (g.away_team_id=? AND g.away_goals < g.home_goals))
    ''', (team_id, player_name, team_dropdown.value, team_dropdown.value))
    goals_per_game_losses = c.fetchall()

    total_goals = sum(goal[1] for goal in goals_per_game)
    average_goals = total_goals / len(goals_per_game)

    total_goals_wins = sum(goal[1] for goal in goals_per_game_wins)
    average_goals_wins = total_goals_wins / len(goals_per_game_wins) if goals_per_game_wins else 0

    total_goals_losses = sum(goal[1] for goal in goals_per_game_losses)
    average_goals_losses = total_goals_losses / len(goals_per_game_losses) if goals_per_game_losses else 0

    colors = ['green', 'red']
    plt.bar(['Total', 'Wins', 'Losses'], [average_goals, average_goals_wins, average_goals_losses], color=colors)
    plt.title(f'Average Goals Per Game for {player_name}')
    plt.ylabel('Goals')
    plt.show()

# Create a button to confirm the player selection
player_button = widgets.Button(description="Confirm Player")
display(player_button)

# Set the function to be called when the player button is clicked
player_button.on_click(display_player_stats)
