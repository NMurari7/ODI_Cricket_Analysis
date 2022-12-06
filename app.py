import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import helper

df = pd.read_csv("analysis_df.csv")

menu_bar = st.sidebar.radio(
    'Select an Option',
    ('Data', 'Overall Analysis', 'Head to Head Analysis', 'Ground Analysis')
)
st.image('ICC.png')
if menu_bar == 'Data':
    st.dataframe(df)

if menu_bar == 'Overall Analysis':
    st.header("TOP STATS")
    # TOTAL STATS
    no_of_matches = df['Match_id'].nunique()
    no_of_countries_hosted = df['Host_Country'].nunique()
    no_of_venues = df['Venue'].nunique()
    no_of_teams = df['Winner'].nunique()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Matches Played")
        st.title(no_of_matches)

    with col2:
        st.subheader("Teams")
        st.title(no_of_teams)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Countries Hosted")
        st.title(no_of_countries_hosted)

    with col2:
        st.subheader("Venues")
        st.title(no_of_venues)

    # PLOTS

    # YEAR WISE
    st.subheader("No. of Matches each year")
    year = helper.overall_year(df)
    x = year.Year
    y = year.Total_Matches
    fig1 = plt.figure(figsize=(14, 8))
    sns.set_style('darkgrid')
    sns.lineplot(x, y)
    plt.xticks(year.Year, rotation='vertical')
    plt.title("Total Matches played each year")

    st.pyplot(fig1)

    # COUNTRY WISE
    st.subheader("No. of Matches Hosted by each countries")
    Host_countries = helper.overall_host_countries(df)
    Host_countries['perc'] = 0


    def get_host_perc(Matches):
        val = round(((Matches * 100) / 3683))
        return val


    Host_countries['perc'] = Host_countries["Matches"].apply(get_host_perc)
    x = Host_countries.iloc[:-3, :]['perc']
    y = Host_countries.iloc[:-3, :]['Country']
    st.dataframe(Host_countries, height=200)
    fig2 = plt.figure(figsize=(14, 8))
    sns.set_style('darkgrid')
    plt.pie(x, labels=y, startangle=45,
            labeldistance=1.05, )
    st.pyplot(fig2)

    #   TEAM WISE WINS VS TOTAL MATCHES PLAYED
    st.subheader("Team wise Total wins vs Total matches played")
    Teams = df["Winner"].unique()
    matches_won_of_total = pd.DataFrame(columns=["Team", "Total_Matches", "Total_Wins"])
    for team in Teams:
        d = helper.overall_wins(df, team)
        #     print(d)
        matches_won_of_total.loc[len(matches_won_of_total)] = d
    st.dataframe(matches_won_of_total, height=200)

    fig3 = plt.figure(figsize=(16, 6))
    sns.set_style('darkgrid')
    plt.bar(matches_won_of_total['Team'], matches_won_of_total['Total_Matches'], label="Total Number of matches played")
    plt.bar(matches_won_of_total['Team'], matches_won_of_total['Total_Wins'], label="Total Number of wins")
    plt.xticks(rotation="vertical")
    plt.title("# of matches played VS # of matches won")
    plt.legend()
    st.pyplot(fig3)

    #   TOTAL MATCHES WON AT HOME OF TOTAL MATCHES PLAYED
    st.subheader("Matches won at Home VS Total matches played")
    Home = pd.DataFrame(columns=["Country", "Total_Matches", "Total_Matches_won"])
    for team in Teams:
        li = helper.overall_home(df, team)
        Home.loc[len(Home)] = li
    st.dataframe(Home, width=600, height=200)
    fig4 = plt.figure(figsize=(16, 8))
    sns.set_style('darkgrid')
    plt.bar(Home.Country, Home.Total_Matches, label="Total Matches played at Home")
    plt.bar(Home.Country, Home.Total_Matches_won, label="Total Matches won at Home")
    plt.xticks(rotation="vertical")
    plt.legend()
    st.pyplot(fig4)

    #   TOTAL MATCHES WON AWAY HOME OF TOTAL MATCHES PLAYED
    st.subheader("Matches won away Home VS Total matches played")
    Away_Home = pd.DataFrame(columns=["Country", "Total_Matches", "Total_Matches_won"])
    for team in Teams:
        li = helper.overall_away(df, team)
        Away_Home.loc[len(Away_Home)] = li

    st.dataframe(Away_Home, width=600, height=200)

    fig5 = plt.figure(figsize=(16, 8))
    sns.set_style('darkgrid')
    plt.bar(Away_Home.Country, Away_Home.Total_Matches, label="Total Matches played away Home")
    plt.bar(Away_Home.Country, Away_Home.Total_Matches_won, label="Total Matches won away Home")
    plt.xticks(rotation="vertical")
    plt.legend()
    st.pyplot(fig5)

    #   VICTORIES EACH YEAR
    st.subheader("Victories each year")
    for team in Teams:
        ydata = helper.overall_hth(df, team)
        if team == 'Australia':
            yearwisewin = ydata

        elif team != 'Australia':
            yearwisewin = yearwisewin.join(ydata)

    sns.set_style('darkgrid')
    fig6 = plt.figure(figsize=(18, 8))
    sns.heatmap(data=yearwisewin.transpose(), annot=True, cmap='Blues', linewidth=.05)
    plt.xlabel('Year', size=15)
    plt.ylabel('Country', size=15)
    plt.title('Victories each Year\n(Country)', size=20)

    st.pyplot(fig6)

if menu_bar == 'Head to Head Analysis':
    countries = df['Winner'].unique()

    team1 = st.selectbox("Select Team 1", countries)
    team2 = st.selectbox("Select Team 2", countries)
    # team1 = "India"
    # team2 = "Pakistan"
    if team1 != team2:
        fig10, fig9, fig8, tota, t1w, t2w, t1_home_wins, t2_home_wins, t1_away_wins, t2_away_wins = helper.head_to_head(
            df, team1, team2)
        st.subheader(f"Total matches played between {team1} and {team2} is {tota}")
        st.subheader("")
        st.markdown(f"{team1} won {t1w} matches and {team2} won {t2w} matches")
        st.pyplot(fig8)
        st.subheader("At Home")
        st.markdown(f"{team1} won {t1_home_wins} matches and {team2} won {t2_home_wins} matches")
        st.pyplot(fig9)
        st.subheader("Away Home")
        st.markdown(f"{team1} won {t1_away_wins} matches and {team2} won {t2_away_wins} matches")
        st.pyplot(fig10)
        st.subheader("\n")
    else:
        st.subheader("Selected same team for Team1 and Team2")

if menu_bar == 'Ground Analysis':
    Venues = df['Venue'].unique()
    Venue_details = pd.DataFrame(columns=["venue", "1st_inng_wins", "2nd_inng_wins", "Total_matches"])
    for venue in Venues:
        li = helper.get_venue_details(df, venue)
        Venue_details.loc[len(Venue_details)] = li
    # st.dataframe(Venue_details)
    ground = st.selectbox("Enter the venue", Venues)

    figg, f, s = helper.plot_ground_bar(Venue_details, ground)
    st.subheader(f"Total no. of matches played at {ground} = {f + s}")
    st.markdown(f"First inning wins are {f} ")
    st.markdown(f"Second inning wins are {s}")
    fig_team = helper.most_team_wins(df, ground)

    st.pyplot(figg)
    st.pyplot(fig_team)
