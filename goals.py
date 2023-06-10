def load_data(db_path):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # Convert SQLite tables to pandas dataframes
    df_players = pd.read_sql_query("SELECT * from Players", conn)
    df_teams = pd.read_sql_query("SELECT id, category from Teams", conn)
    
    # Filter out players with 0 goals
    df_players = df_players[df_players['goals'] != 0]
    
    # Merge player and team dataframes on team_id
    df = pd.merge(df_players, df_teams, left_on='team_id', right_on='id', suffixes=('_player', '_team'))

    return df, conn

def visualize_distribution(df):
    categories = df['category'].unique()
    for category in categories:
        df_category = df[df['category'] == category]

        # Group players by the total number of goals and count the number of players in each group
        goals_distribution = df_category.groupby('id_player')['goals'].sum().value_counts().reset_index()
        
        goals_distribution.columns = ['Total Goals', 'Number of Players']

        # Sort the dataframe by the total number of goals
        goals_distribution = goals_distribution.sort_values('Total Goals')

        # Plot the distribution of goals with increased space between bars and wider bars
        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=goals_distribution, x='Total Goals', y='Number of Players', color='blue', alpha=0.8, saturation=0.8, errorbar=None, width=0.9)

        plt.title(f'Distribution of Goals for {category} category')
        plt.xlabel('Total Goals')
        plt.ylabel('Number of Players')

        # Rotate x-axis tick labels
        plt.xticks(rotation=90, fontsize=6)  # Set the font size of x-axis tick labels

        # Add a reference line for 1/x distribution
        max_goals_histogram = goals_distribution['Total Goals'].iloc[-1]  # Maximum number of goals in the histogram
        max_players = goals_distribution['Number of Players'].max()  # Maximum number of players for a certain goal count
        x = np.arange(1, max_goals_histogram + 1)  # X values for the 1/x distribution
        a = 0.005  # This can be any non-zero positive value
        b = 0.9  # This controls the steepness of the curve; values less than 1 make the curve less steep
        y = a / (x + b)**b * max_players  # 1/x distribution with a steepness parameter
        y = y / y.max() * max_players  # Scale the 1/x distribution so that its peak matches the peak of the histogram

        # Limit the x-values and y-values to match the last bar of the histogram
        x = x[:len(goals_distribution)]
        y = y[:len(goals_distribution)]
        
        plt.plot(x, y, color='red', linestyle='--', linewidth=2)

        plt.show()

        # Print the text version of the histogram
        print("Text Version of Histogram for", category, "category:")
        for index, row in goals_distribution.iterrows():
            print(f"{row['Total Goals']} goals: {row['Number of Players']:,} players")
            
if __name__ == "__main__":
    db_path = 'fighDB.db'  # TODO: Replace with the path to your SQLite database

    df, conn = load_data(db_path)
    visualize_distribution(df)

    # Close the connection
    conn.close()
