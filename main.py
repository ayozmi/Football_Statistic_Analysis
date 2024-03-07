import streamlit as st
import pandas as pd
import sqlite3
import base64
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from mplsoccer import PyPizza
from highlight_text import fig_text


def load_data():
    """Load data from the SQL database."""
    # Assuming the data directory is at the root level of your project
    conn = sqlite3.connect('data/database.sqlite')  # Updated path to the database
    df = pd.read_sql_query("SELECT * FROM statistics", conn)
    conn.close()
    return df


def set_background(png_file):
    """Set a background image for the Streamlit app."""
    # Adjusted to use a relative path from main.py location
    with open(f"{png_file}", "rb") as image_file:  # Corrected path
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def compare_players(player_1, player_2, df, df_player):
    # parameter and values list
    # The values are taken from the excellent fbref website (supplied by StatsBomb)
    params = [
        "goals", "xGoals", "assists",
        "xAssists", "xGoalsBuildup",
        "xGoalsChain"
    ]
    params_offset = [
        True, True, True, True, True, True
    ]

    player_name_1 = df_player["name"][df_player["playerID"] == player_1].iloc[0]
    player_name_2 = df_player["name"][df_player["playerID"] == player_2].iloc[0]
    df_player = (df.groupby("playerID")[params].mean().reset_index())
    df_player1_agg = df_player[params][df_player["playerID"] == player_1]
    df_player2_agg = df_player[params][df_player["playerID"] == player_2]
    # st.write(df_player1_agg)
    # st.write(df_player2_agg)
    df_player1_agg[params] *= 100
    df_player2_agg[params] *= 100
    df_player1_agg = df_player1_agg.round(2)
    df_player2_agg = df_player2_agg.round(2)
    # instantiate PyPizza class
    baker = PyPizza(
        params=params,  # list of parameters
        background_color="#EBEBE9",  # background color
        straight_line_color="#222222",  # color for straight lines
        straight_line_lw=1,  # linewidth for straight lines
        last_circle_lw=1,  # linewidth of last circle
        last_circle_color="#222222",  # color of last circle
        other_circle_ls="-.",  # linestyle for other circles
        other_circle_lw=1  # linewidth for other circles
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        df_player1_agg.iloc[0].tolist(),  # list of values
        compare_values=df_player2_agg.iloc[0].tolist(),  # comparison values
        figsize=(8, 8),  # adjust figsize according to your need
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#222222",
            zorder=2, linewidth=1
        ),  # values to be used when plotting slices
        kwargs_compare=dict(
            facecolor="#FF9300", edgecolor="#222222",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#000000", fontsize=12
        ),  # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=12,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        ),  # values to be used when adding parameter-values labels
        kwargs_compare_values=dict(
            color="#000000", fontsize=12,
            bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
        ),  # values to be used when adding parameter-values labels
    )

    # adjust text for comparison-values-text
    baker.adjust_texts(params_offset, offset=-0.3, adj_comp_values=True)

    fig_text(
        0.515, 0.99, f"<{player_name_1}> vs <{player_name_2}>", size=17, fig=fig,
        highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
        ha="center", color="#000000"
    )

    # add subtitle
    fig.text(
        0.515, 0.942,
        "2014/2020",
        size=15,
        ha="center", color="#000000"
    )
    return plt


def plot_stats(name_stat, df_team_stats_names):
    df_team_stats_grouped = df_team_stats_names.groupby("name").agg({
        'goals': 'sum',
        'shots': 'sum',
        'fouls': 'sum',
        'xGoals': 'sum',
        'shotsOnTarget': 'sum',
        'ppda': 'mean',
        'yellowCards': 'sum',
        'redCards': 'sum'
    })
    group_df_sorted = df_team_stats_grouped.sort_values(by=name_stat, ascending=False)
    top_teams = group_df_sorted.head(10)
    bottom_teams = group_df_sorted.tail(10)
    plt.figure(figsize=(15, 11))
    plt.bar(top_teams.index, top_teams[name_stat], color='blue', label='Top 10')
    plt.bar(bottom_teams.index, bottom_teams[name_stat], color='red', label='Bottom 10')
    plt.xlabel('Team')
    plt.ylabel(name_stat)
    # plt.title('Total Goals Scored by Top and Bottom 10 Teams')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)


def main():
    set_background('data/images/football.jpg')  # Ensure the path is corrected for the new structure
    st.title('Football Statistic Analysis! ⚽')
    st.write(
        "Football, is considered by many the world's game, "
        "captivating millions of fans with its exhilarating matches and dynamic gameplay. "
        "Behind every thrilling match lies a treasure trove of "
        "data and statistics that offer insights into team and player performance, "
        "strategy effectiveness, and the overall dynamics of the game.")
    st.subheader("Let's start with the anthem of the best football team in the world!")
    st.audio("data/audio/fc_barcelona.mp3")
    st.write("I get chills everytime I listen to this anthem.")
    st.subheader("Goals of this analysis:")
    st.write("In this analysis, we  will embark on a journey to explore the "
             "fascinating world of football statistics using the power of "
             "Python programming language and its data analysis libraries. "
             "Through this analysis, we aim to uncover valuable insights, trends, and patterns "
             "hidden within football data, providing a deeper understanding of the game we all love.")
    st.write("For this analysis, we will be using the data from the Football Database found in Kaggle.")
    st.markdown('Link to the data source: '
                '[Football Database](https://www.kaggle.com/datasets/technika148/football-database/data)',
                unsafe_allow_html=True)
    st.write("This dataset contains football-related data covering the Top 5 leagues in Europe from 2014-2020.")
    with (st.container()):
        styled_container = f"""
        <style>
            .stContainer {{
                background-color: rgba(255, 255, 255, 0.5); /* Semi-transparent white */
                border-radius: 15px;
                padding: 10px;
            }}
        </style>
        """
        st.markdown(styled_container, unsafe_allow_html=True)

        # Load and display the data within the styled container
        # df = load_data()
        # st.write(df)

        # Display a video from a URL within the styled container
        # st.video('https://www.youtube.com/watch?v=0eOf-EOCzuw')
        df_appearance = pd.read_csv('data/raw/appearances.csv')
        df_game = pd.read_csv('data/raw/games.csv')
        df_shots = pd.read_csv('data/raw/shots.csv')
        df_team_stats = pd.read_csv('data/raw/teamstats.csv')

        # We need to make the result of each game numerical
        df_team_stats['result'] = df_team_stats['result'].map({'W': 1, 'L': 0, 'D': 2})
        df_team_stats_game = df_team_stats.groupby("gameID")["goals"].sum().reset_index()
        goals_frequency = df_team_stats_game['goals'].value_counts().sort_index().reset_index()
        goals_frequency.columns = ['Number of goals', 'Frequency']
        fig = px.bar(goals_frequency, x='Number of goals', y='Frequency',
                     labels={'Number of goals': 'Number of goals', 'Frequency': 'Frequency'})
        fig.update_layout(xaxis=dict(title='Number of goals per game'),
                          yaxis=dict(title='Number of games'))

        fig.update_layout(xaxis_title='Number of goals per game', yaxis_title='Number of games')
        st.write("Let's explore some statistics from our dataset. "
                 "Let's start by seeing what's the most frequent number of goals scored per game:")
        st.plotly_chart(fig)
        st.write("As we can see, the most frequent number of goals scored per game is two, "
                 "the number of games where 2 goals were scored is just a bit more than 3000. "
                 "After that we have 3 goals per game as the second most frequent number of goals scored per game."
                 "But the most interesting fact from this plot is that there are more games"
                 " with 5 goals than games with 0 goals.")
        st.write("Now I don't know about you, but personnally I feel like football became more defensive. "
                 "After many years in their prime, Leo Messi and Cristiano Ronaldo "
                 "don't score as much as they used to and it became rarer than ever to see incredible scorlines."
                 " Now since we have the data between our hands we can explore this theory and confirm or deny it.")
        st.write("Let's see if the game became more defensive or not:")
        df_team_stats_season = df_team_stats.groupby("season")["goals"].sum().reset_index()
        fig = px.bar(df_team_stats_season,
                     x='season',
                     y='goals',
                     labels={'season': 'Season', 'goals': 'Number of goals per season'},
                     hover_name='goals',
                     hover_data={'season': False, 'goals': True})

        fig.update_layout(xaxis_title='Season', yaxis_title='Number of goals per season')
        st.plotly_chart(fig)
        df_team_stats_season = df_team_stats.groupby("season")["goals"].max().reset_index()
        st.write(
            "Thanks to this graph, we can see that the game didn't become more defensive, "
            "as the 2020 season has the second most goals per season. "
            "The 2019 season however is low, but we need to take into account that because of COVID 19, "
            "the French league (Ligue 1) suspended football indefinitely on March 13 2020, "
            "which makes the stat for the "
            "2019 season inaccurate.")
        # st.write(df_team_stats_season["goals"])
        df_league = pd.read_csv("data/raw/leagues.csv")
        df_team_stats_league = pd.merge(df_team_stats, df_game, on="gameID", how="inner")
        df_team_stats_league = pd.merge(df_team_stats_league, df_league, on="leagueID", how="inner")
        df_team_stats_league_grouped = df_team_stats_league.groupby("name")["goals"].sum().reset_index()
        fig = px.bar(df_team_stats_league_grouped,
                     x='name',
                     y='goals',
                     labels={'name': 'League', 'goals': 'Number of goals per league'},
                     hover_name='goals',
                     hover_data={'name': False, 'goals': True})

        fig.update_layout(xaxis_title='League Name', yaxis_title='Number of goals per league')
        st.write("One of the things that every football fan love doing is comparing. "
                 "Comparing their favorite team, or football player or even leagues. "
                 "What I love with statistics is you can actually backup your claims with proof.")
        # # <editor-fold desc="Compare Leagues">
        # st.write("I always heard that the Premier League is the best league in the world. "
        #          "How can we check if this sentence is true or false? "
        #          "Well for me what makes a league better than the other one is the quality of the teams. "
        #          "For others a metric that could be relevant is the number of goals scored, and I can understand"
        #          "that people prefrer watching attacking football strategy.")
        # st.write("So let's see the number of goals scored in each league to determine "
        #          "which one has a offensive gamestyle.")
        # st.plotly_chart(fig)
        # st.write("As we can see from this graph, Serie A has more goals than the other leagues, "
        #          "however let's keep in mind that the number of games in the Bundesliga is lower ,and "
        #          "also the fact that Ligue 1 didn't complete the 2019 Season. "
        #          "A better metric to see which league is more offensive then would be goals per game.")
        #
        # games_per_league = df_team_stats_league.groupby("name")["gameID"].count().reset_index()
        # st.write(games_per_league)
        # df_goals_games_per_league = pd.merge(df_team_stats_league, games_per_league, on="name", how="inner")
        # df_goals_games_per_league['goals_per_game'] = df_goals_games_per_league['goals'] / df_goals_games_per_league[
        #     'gameID_x']
        # fig = px.bar(df_goals_games_per_league,
        #              x='name',
        #              y='goals_per_game',
        #              labels={'name': 'League', 'goals': 'Number of goals per league per game'},
        #              hover_name='goals_per_game',
        #              hover_data={'name': False, 'goals_per_game': True})
        # fig.update_layout(xaxis_title='League Name', yaxis_title='Number of goals per game per league')
        # st.plotly_chart(fig)
        # # </editor-fold>
        # <editor-fold desc="Correlation Stats and Result">
        st.write(
            "But before we start comparing, it is important to understand how important each stat is, "
            "so first let's start with a correlation between each stat and the match outcome.")
        # Calculate the correlation coefficients between each statistic and the result
        stats = ["goals", "xGoals", "shots", "shotsOnTarget", "deep", "ppda", "fouls", "corners", "yellowCards",
                 "redCards"]
        correlation_with_result = df_team_stats[stats].apply(lambda x: x.corr(df_team_stats['result']))

        # Plot the correlation coefficients
        plt.figure(figsize=(15, 11))
        sns.barplot(x=correlation_with_result.index, y=correlation_with_result.values)
        plt.title('Correlation with Match Outcome')
        plt.xlabel('Statistic')
        plt.ylabel('Correlation Coefficient')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        st.write("As we can see here, some stats have a strong correlation with the match outcome. "
                 "Some are pretty obvious, but others not that much. "
                 "Obviously the number of goals scored in a match has a strong correlation "
                 "with the match outcome since the more you score the more chances you have to "
                 "win the game. However I was surprised to see that there is no strong correlation "
                 "between the number of yellow cards and the match outcome. "
                 "I would have thought that a team who is struggling will commit more fouls "
                 "and therefore have more yellow cards, but as shown above it is not the case "
                 "which means that yellow cards are not a good stat to use to determine struggling teams.")
        # </editor-fold>
        # <editor-fold desc="Correlation Matrix">
        st.write("It is also important to understand the correlation between each stat, "
                 "and how strong that correlation is."
                 " Let's look at this using a correlation Matrix:")
        correlation = df_team_stats[stats].corr()
        sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)
        plt.title('Correlation Matrix')
        plt.xticks(rotation=0)
        st.pyplot(plt)
        # </editor-fold>
        # <editor-fold desc="Compare teams">
        st.write("At the end of the day football game is about winning. And to win, "
                 "you need to outscore your opponent, "
                 "let's compare the teams of the top 5 league using the most "
                 "important metric in the game: Goals.")
        st.write("We will display a graph showing the top and bottom 10 clubs by goals in the top 5 competitions:")
        df_team = pd.read_csv("data/raw/teams.csv")
        df_team_stats_names = pd.merge(df_team_stats, df_team, on="teamID", how="inner")
        df_team_stats_grouped = df_team_stats_names.groupby("name").agg({
            'goals': 'sum',
            'shots': 'sum',
            'fouls': 'sum',
            'xGoals': 'sum',
            'shotsOnTarget': 'sum',
            'ppda': 'mean',
            'yellowCards': 'sum',
            'redCards': 'sum'
        })
        plot_stats("goals", df_team_stats_grouped)
        st.write("As we can see, the top team in this period of time when it comes to scoring goals is "
                 "FC Barcelona followed by PSG and then Bayern Munich.")
        # </editor-fold>
        # <editor-fold desc="Compare players">
        df_players = pd.read_csv("data/raw/players.csv", encoding="latin1")
        option1_selected = st.selectbox('Football Player 1', df_players['playerID'],
                                        format_func=lambda x: df_players[df_players['playerID'] == x]['name'].values[
                                            0], index=2034)
        option2_selected = st.selectbox('Football Player 2', df_players['playerID'],
                                        format_func=lambda x: df_players[df_players['playerID'] == x]['name'].values[
                                            0], index=2061)
        fig = compare_players(option1_selected, option2_selected, df_appearance, df_players)
        st.pyplot(fig)
        # </editor-fold>


if __name__ == '__main__':
    main()
