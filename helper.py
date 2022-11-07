import matplotlib.pyplot as plt


def overall_year(df):
    year = df['Year'].value_counts().sort_values(ascending=False).reset_index()
    year.columns = ["Year", "Total_Matches"]
    return year


def overall_host_countries(df):
    H_c = df['Host_Country'].value_counts().reset_index()
    H_c.columns = ["Country", "Matches"]
    return H_c


def overall_wins(df, team):
    total_matches = df[(df['Team 1'] == team) | (df['Team 2'] == team)]
    total_wins = df[df["Winner"] == team]
    tot_wins, c = total_wins.shape
    matches_played, cols = total_matches.shape
    #     d = {"Team":team, "Total_Matches":matches_played,"Total_Wins":tot_wins}
    d = [team, matches_played, tot_wins]
    return d


def overall_home(df, team):
    home = df[((df['Team 1'] == team) | (df['Team 2'] == team)) & (df['Host_Country'] == team)]
    home_won = df[
        ((df["Team 1"] == team) | (df['Team 2'] == team)) & (df['Host_Country'] == team) & (df['Winner'] == team)]
    wrows, wcols = home_won.shape
    rows, cols = home.shape
    return [team, rows, wrows]


def overall_away(df, team):
    home = df[((df['Team 1'] == team) | (df['Team 2'] == team)) & (df['Host_Country'] != team)]
    home_won = df[
        ((df["Team 1"] == team) | (df['Team 2'] == team)) & (df['Host_Country'] != team) & (df['Winner'] == team)]
    arows, wcols = home_won.shape
    rows, cols = home.shape
    return [team, rows, arows]


def overall_hth(df, country):
    data = df.loc[df.Winner == country].groupby('Year').apply(lambda p: p.Winner.value_counts())
    return data


def head_to_head(df, t1, t2):
    vs = df[((df["Team 1"] == t1) | (df["Team 2"] == t1)) & ((df["Team 1"] == t2) | (df["Team 2"] == t2))]
    tota, sd = vs.shape
    # TEAM 1
    t1_wins = vs[vs["Winner"] == t1]  # t1 wins df
    t1w, x = t1_wins.shape  # No. of wins by t1
    t1_home = t1_wins[t1_wins["Host_Country"] == t1]
    t1_away = t1_wins[t1_wins["Host_Country"] != t1]

    t1_home_wins, c = t1_home.shape  # t1 total no. of wins vs t2 at home
    t1_away_wins, cl = t1_away.shape  # t1 total no. of wins vs t2 at away home

    # TEAM 2
    t2_wins = vs[vs["Winner"] == t2]  # t2 wins df
    t2w, y = t2_wins.shape  # No. of wins by t2
    t2_home = t2_wins[t2_wins["Host_Country"] == t2]
    t2_away = t2_wins[t2_wins["Host_Country"] != t2]
    t2_home_wins, cs = t2_home.shape  # t2 total no. of wins vs t1 at home
    t2_away_wins, cc = t2_away.shape  # t2 total no. of wins vs t1 at away home

    draws = vs[(vs["Winner"] != t1) & (vs["Winner"] != t2)]
    ds = draws.shape  # Total no. of draws if any

    #     PLOTS

    print(f"Total no. of matches played between {t1} and {t2} is {tota}")

    fig8 = plt.figure(figsize=(16, 6))
    plt.bar(t1, t1w)
    plt.bar(t2, t2w)
    plt.title(f"{t1} VS {t2}  head-to-head wins")


    fig9 = plt.figure(figsize=(16, 6))
    plt.bar(t1, t1_home_wins)
    plt.bar(t2, t2_home_wins)
    plt.title(f"{t1} and {t2} wins at home")


    fig10 = plt.figure(figsize=(16, 6))
    plt.bar(t1, t1_away_wins)
    plt.bar(t2, t2_away_wins)
    plt.title(f"{t1} and {t2} wins away home")


    return (fig10, fig9, fig8, tota, t1w, t2w, t1_home_wins, t2_home_wins, t1_away_wins, t2_away_wins)


def get_venue_details(df,venue):
    first_wins  = df[ (df["Venue"] == venue)  & (df['Winners_inng'] == 1)]
    second_wins = df[ (df["Venue"] == venue)  & (df['Winners_inng'] == 2)]
    frows , c = first_wins.shape
    srows, co = second_wins.shape
    return [venue,frows, srows,frows+srows]


def plot_ground_bar(Venue_details, venue):
    v = Venue_details[Venue_details["venue"] == venue]
    name = v['venue'].values[0]
    f = v['1st_inng_wins'].values[0]
    s = v['2nd_inng_wins'].values[0]
    print(f"Total no. of matches played in {venue} is {f + s}")

    figg = plt.figure()
    # sns.set_style('darkgrid')
    plt.bar(['1st_inng_wins'], f, width=0.4)
    plt.bar(['2nd_inng_wins'], s, width=0.4)
    plt.title(venue)


    return (figg, f, s)

    # if f > s:
    #     print("Choose To Bat First")
    # elif f == s:
    #     print("1st inng wins = 2nd inng wins")
    # else:
    #     print("Choose To Bowl First")
