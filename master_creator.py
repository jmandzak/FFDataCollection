import pandas as pd


def main():
    # grab strength of schedules
    full_df = pd.read_csv("sos_full.csv")
    season_df = pd.read_csv("sos_season.csv")
    playoff_df = pd.read_csv("sos_playoff.csv")
    full_df.set_index("TEAM", inplace=True)
    season_df.set_index("TEAM", inplace=True)
    playoff_df.set_index("TEAM", inplace=True)
    full = full_df.to_dict("index")
    season = season_df.to_dict("index")
    playoff = playoff_df.to_dict("index")

    # grab boom/bust/start
    all_boom_df = pd.read_csv("all_boom_bust.csv")
    all_boom_df.set_index("PLAYER NAME", inplace=True)
    all_boom_bust = all_boom_df.to_dict("index")

    # grab depth chart
    depth_df = pd.read_csv("all_depth_chart.csv")
    depth_df.set_index("PLAYER NAME", inplace=True)
    depth_chart = depth_df.to_dict("index")

    # this dict will be used later for adding positions to everyone
    player_positions = {}

    # function used for combining dataframes
    arbitrary_func = lambda s1, s2: s1 if s1.isnull().sum() <= s2.isnull().sum() else s2

    # Let's do this by positions
    # First, we'll start with QBs
    qb_avg_df = pd.read_csv("qb_avg_stats.csv")
    qb_avg_df.set_index("PLAYER NAME", inplace=True)

    qb_rank_df = pd.read_csv("qb_rank_stats.csv")
    qb_rank_df.set_index("PLAYER NAME", inplace=True)

    qb_total_df = pd.read_csv("qb_total_stats.csv")
    qb_total_df.set_index("PLAYER NAME", inplace=True)

    qb_df = qb_avg_df.combine(qb_total_df, arbitrary_func)
    qb_df = qb_df.drop(["POS_RK", "POS_TIERS", "TEAM"], axis=1)
    qb_df = qb_df.combine(qb_rank_df, arbitrary_func)
    qb_df = qb_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )

    qb_df.dropna(inplace=True, subset=["TEAM"])

    # assign strength of schedule and boom/bust/start
    playoff_sos = []
    season_sos = []
    full_sos = []
    boom = []
    bust = []
    starter = []
    ppr_boom = []
    ppr_bust = []
    ppr_starter = []
    depth = []

    for index, row in qb_df.iterrows():
        player_positions[index] = "QB"
        if row["TEAM"] == "FA":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]]["QB"])
            season_sos.append(season[row["TEAM"]]["QB"])
            full_sos.append(full[row["TEAM"]]["QB"])

        if index in all_boom_bust:
            boom.append(all_boom_bust[index]["BOOM"])
            bust.append(all_boom_bust[index]["BUST"])
            starter.append(all_boom_bust[index]["STARTER"])
            ppr_boom.append(all_boom_bust[index]["PPR_BOOM"])
            ppr_bust.append(all_boom_bust[index]["PPR_BUST"])
            ppr_starter.append(all_boom_bust[index]["PPR_STARTER"])
        else:
            boom.append(0)
            bust.append(0)
            starter.append(0)
            ppr_boom.append(0)
            ppr_bust.append(0)
            ppr_starter.append(0)

        if index in depth_chart:
            depth.append(depth_chart[index]["DEPTH"])
        else:
            depth.append(0)

    qb_df["FULL_SOS"] = full_sos
    qb_df["SEASON_SOS"] = season_sos
    qb_df["PLAYOFF_SOS"] = playoff_sos
    qb_df["BOOM"] = boom
    qb_df["BUST"] = bust
    qb_df["STARTER"] = starter
    qb_df["PPR_BOOM"] = ppr_boom
    qb_df["PPR_BUST"] = ppr_bust
    qb_df["PPR_STARTER"] = ppr_starter
    qb_df["DEPTH"] = depth
    qb_df.to_csv("final/qbs.csv")

    # Now on to RBs
    rb_avg_df = pd.read_csv("rb_avg_stats.csv")
    rb_avg_df.set_index("PLAYER NAME", inplace=True)

    rb_ppr_avg_df = pd.read_csv("rb_ppr_avg_stats.csv")
    rb_ppr_avg_df.set_index("PLAYER NAME", inplace=True)

    rb_ppr_rank_df = pd.read_csv("rb_ppr_rank_stats.csv")
    rb_ppr_rank_df.set_index("PLAYER NAME", inplace=True)

    rb_ppr_total_df = pd.read_csv("rb_ppr_total_stats.csv")
    rb_ppr_total_df.set_index("PLAYER NAME", inplace=True)

    rb_rank_df = pd.read_csv("rb_rank_stats.csv")
    rb_rank_df.set_index("PLAYER NAME", inplace=True)

    rb_total_df = pd.read_csv("rb_total_stats.csv")
    rb_total_df.set_index("PLAYER NAME", inplace=True)

    rb_df = rb_avg_df.combine(rb_ppr_avg_df, arbitrary_func)
    rb_df = rb_df.combine(rb_ppr_total_df, arbitrary_func)
    rb_df = rb_df.combine(rb_total_df, arbitrary_func)
    rb_df = rb_df.drop(["PPR_POS_RK", "PPR_POS_TIERS", "TEAM"], axis=1)
    rb_df = rb_df.combine(rb_rank_df, arbitrary_func)
    rb_df = rb_df.combine(rb_ppr_rank_df, arbitrary_func)
    rb_df = rb_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "PPR_AVG.": "PPR_AVG_RK",
            "PPR_BEST": "PPR_BEST_RK",
            "PPR_STD.DEV": "PPR_STD.DEV_RK",
            "PPR_WORST": "PPR_WORST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )

    # assign strength of schedule
    playoff_sos = []
    season_sos = []
    full_sos = []
    boom = []
    bust = []
    starter = []
    ppr_boom = []
    ppr_bust = []
    ppr_starter = []
    depth = []

    rb_df = rb_df.dropna(subset=["TEAM"])
    # drop duplicates
    rb_df = rb_df[~rb_df.index.duplicated(keep="first")]

    for index, row in rb_df.iterrows():
        player_positions[index] = "RB"
        if row["TEAM"] == "FA":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]]["RB"])
            season_sos.append(season[row["TEAM"]]["RB"])
            full_sos.append(full[row["TEAM"]]["RB"])

        if index in all_boom_bust:
            boom.append(all_boom_bust[index]["BOOM"])
            bust.append(all_boom_bust[index]["BUST"])
            starter.append(all_boom_bust[index]["STARTER"])
            ppr_boom.append(all_boom_bust[index]["PPR_BOOM"])
            ppr_bust.append(all_boom_bust[index]["PPR_BUST"])
            ppr_starter.append(all_boom_bust[index]["PPR_STARTER"])
        else:
            boom.append(0)
            bust.append(0)
            starter.append(0)
            ppr_boom.append(0)
            ppr_bust.append(0)
            ppr_starter.append(0)

        if index in depth_chart:
            depth.append(depth_chart[index]["DEPTH"])
        else:
            depth.append(0)

    rb_df["FULL_SOS"] = full_sos
    rb_df["SEASON_SOS"] = season_sos
    rb_df["PLAYOFF_SOS"] = playoff_sos
    rb_df["BOOM"] = boom
    rb_df["BUST"] = bust
    rb_df["STARTER"] = starter
    rb_df["PPR_BOOM"] = ppr_boom
    rb_df["PPR_BUST"] = ppr_bust
    rb_df["PPR_STARTER"] = ppr_starter
    rb_df["DEPTH"] = depth
    rb_df.to_csv("final/rbs.csv")

    # Now WRs
    wr_avg_df = pd.read_csv("wr_avg_stats.csv")
    wr_avg_df.set_index("PLAYER NAME", inplace=True)

    wr_ppr_avg_df = pd.read_csv("wr_ppr_avg_stats.csv")
    wr_ppr_avg_df.set_index("PLAYER NAME", inplace=True)

    wr_ppr_rank_df = pd.read_csv("wr_ppr_rank_stats.csv")
    wr_ppr_rank_df.set_index("PLAYER NAME", inplace=True)

    wr_ppr_total_df = pd.read_csv("wr_ppr_total_stats.csv")
    wr_ppr_total_df.set_index("PLAYER NAME", inplace=True)

    wr_rank_df = pd.read_csv("wr_rank_stats.csv")
    wr_rank_df.set_index("PLAYER NAME", inplace=True)

    wr_total_df = pd.read_csv("wr_total_stats.csv")
    wr_total_df.set_index("PLAYER NAME", inplace=True)

    wr_df = wr_avg_df.combine(wr_ppr_avg_df, arbitrary_func)
    wr_df = wr_df.combine(wr_ppr_total_df, arbitrary_func)
    wr_df = wr_df.combine(wr_total_df, arbitrary_func)
    wr_df = wr_df.drop(["PPR_POS_RK", "PPR_POS_TIERS", "TEAM"], axis=1)
    wr_df = wr_df.combine(wr_rank_df, arbitrary_func)
    wr_df = wr_df.combine(wr_ppr_rank_df, arbitrary_func)
    wr_df = wr_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "PPR_AVG.": "PPR_AVG_RK",
            "PPR_BEST": "PPR_BEST_RK",
            "PPR_STD.DEV": "PPR_STD.DEV_RK",
            "PPR_WORST": "PPR_WORST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )

    wr_df.dropna(inplace=True, subset=["TEAM"])
    # drop duplicates
    wr_df = wr_df[~wr_df.index.duplicated(keep="first")]

    # assign strength of schedule
    playoff_sos = []
    season_sos = []
    full_sos = []
    boom = []
    bust = []
    starter = []
    ppr_boom = []
    ppr_bust = []
    ppr_starter = []
    depth = []

    for index, row in wr_df.iterrows():
        player_positions[index] = "WR"
        if row["TEAM"] == "FA":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]]["WR"])
            season_sos.append(season[row["TEAM"]]["WR"])
            full_sos.append(full[row["TEAM"]]["WR"])

        if index in all_boom_bust:
            boom.append(all_boom_bust[index]["BOOM"])
            bust.append(all_boom_bust[index]["BUST"])
            starter.append(all_boom_bust[index]["STARTER"])
            ppr_boom.append(all_boom_bust[index]["PPR_BOOM"])
            ppr_bust.append(all_boom_bust[index]["PPR_BUST"])
            ppr_starter.append(all_boom_bust[index]["PPR_STARTER"])
        else:
            boom.append(0)
            bust.append(0)
            starter.append(0)
            ppr_boom.append(0)
            ppr_bust.append(0)
            ppr_starter.append(0)

        if index in depth_chart:
            depth.append(depth_chart[index]["DEPTH"])
        else:
            depth.append(0)

    wr_df["FULL_SOS"] = full_sos
    wr_df["SEASON_SOS"] = season_sos
    wr_df["PLAYOFF_SOS"] = playoff_sos
    wr_df["BOOM"] = boom
    wr_df["BUST"] = bust
    wr_df["STARTER"] = starter
    wr_df["PPR_BOOM"] = ppr_boom
    wr_df["PPR_BUST"] = ppr_bust
    wr_df["PPR_STARTER"] = ppr_starter
    wr_df["DEPTH"] = depth
    wr_df.to_csv("final/wrs.csv")

    # Now TEs
    te_avg_df = pd.read_csv("te_avg_stats.csv")
    te_avg_df.set_index("PLAYER NAME", inplace=True)

    te_ppr_avg_df = pd.read_csv("te_ppr_avg_stats.csv")
    te_ppr_avg_df.set_index("PLAYER NAME", inplace=True)

    te_ppr_rank_df = pd.read_csv("te_ppr_rank_stats.csv")
    te_ppr_rank_df.set_index("PLAYER NAME", inplace=True)

    te_ppr_total_df = pd.read_csv("te_ppr_total_stats.csv")
    te_ppr_total_df.set_index("PLAYER NAME", inplace=True)

    te_rank_df = pd.read_csv("te_rank_stats.csv")
    te_rank_df.set_index("PLAYER NAME", inplace=True)

    te_total_df = pd.read_csv("te_total_stats.csv")
    te_total_df.set_index("PLAYER NAME", inplace=True)

    te_df = te_avg_df.combine(te_ppr_avg_df, arbitrary_func)
    te_df = te_df.combine(te_ppr_total_df, arbitrary_func)
    te_df = te_df.combine(te_total_df, arbitrary_func)
    te_df = te_df.drop(["PPR_POS_RK", "PPR_POS_TIERS", "TEAM"], axis=1)
    te_df = te_df.combine(te_rank_df, arbitrary_func)
    te_df = te_df.combine(te_ppr_rank_df, arbitrary_func)
    te_df = te_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "PPR_AVG.": "PPR_AVG_RK",
            "PPR_BEST": "PPR_BEST_RK",
            "PPR_STD.DEV": "PPR_STD.DEV_RK",
            "PPR_WORST": "PPR_WORST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )

    te_df.dropna(inplace=True, subset=["TEAM"])
    # drop duplicates
    te_df = te_df[~te_df.index.duplicated(keep="first")]

    # assign strength of schedule
    playoff_sos = []
    season_sos = []
    full_sos = []
    boom = []
    bust = []
    starter = []
    ppr_boom = []
    ppr_bust = []
    ppr_starter = []
    depth = []

    for index, row in te_df.iterrows():
        player_positions[index] = "TE"
        if row["TEAM"] == "FA":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]]["TE"])
            season_sos.append(season[row["TEAM"]]["TE"])
            full_sos.append(full[row["TEAM"]]["TE"])

        if index in all_boom_bust:
            boom.append(all_boom_bust[index]["BOOM"])
            bust.append(all_boom_bust[index]["BUST"])
            starter.append(all_boom_bust[index]["STARTER"])
            ppr_boom.append(all_boom_bust[index]["PPR_BOOM"])
            ppr_bust.append(all_boom_bust[index]["PPR_BUST"])
            ppr_starter.append(all_boom_bust[index]["PPR_STARTER"])
        else:
            boom.append(0)
            bust.append(0)
            starter.append(0)
            ppr_boom.append(0)
            ppr_bust.append(0)
            ppr_starter.append(0)

        if index in depth_chart:
            depth.append(depth_chart[index]["DEPTH"])
        else:
            depth.append(0)

    te_df["FULL_SOS"] = full_sos
    te_df["SEASON_SOS"] = season_sos
    te_df["PLAYOFF_SOS"] = playoff_sos
    te_df["BOOM"] = boom
    te_df["BUST"] = bust
    te_df["STARTER"] = starter
    te_df["PPR_BOOM"] = ppr_boom
    te_df["PPR_BUST"] = ppr_bust
    te_df["PPR_STARTER"] = ppr_starter
    te_df["DEPTH"] = depth
    te_df.to_csv("final/tes.csv")

    # Now DEFs
    def_avg_df = pd.read_csv("def_avg_stats.csv")
    def_avg_df.set_index("PLAYER NAME", inplace=True)

    def_rank_df = pd.read_csv("def_rank_stats.csv")
    def_rank_df.set_index("PLAYER NAME", inplace=True)

    def_total_df = pd.read_csv("def_total_stats.csv")
    def_total_df.set_index("PLAYER NAME", inplace=True)

    def_df = def_avg_df.combine(def_rank_df, arbitrary_func)
    def_df = def_df.combine(def_total_df, arbitrary_func)
    def_df = def_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )

    # assign strength of schedule
    playoff_sos = []
    season_sos = []
    full_sos = []
    for index, row in def_df.iterrows():
        player_positions[index] = "DEF"
        if row["TEAM"] == "FA":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]]["DEF"])
            season_sos.append(season[row["TEAM"]]["DEF"])
            full_sos.append(full[row["TEAM"]]["DEF"])

    def_df["FULL_SOS"] = full_sos
    def_df["SEASON_SOS"] = season_sos
    def_df["PLAYOFF_SOS"] = playoff_sos
    def_df.to_csv("final/defs.csv")

    # And finally kickers
    k_avg_df = pd.read_csv("k_avg_stats.csv")
    k_avg_df.set_index("PLAYER NAME", inplace=True)

    k_rank_df = pd.read_csv("k_rank_stats.csv")
    k_rank_df.set_index("PLAYER NAME", inplace=True)

    k_total_df = pd.read_csv("k_total_stats.csv")
    k_total_df.set_index("PLAYER NAME", inplace=True)

    k_df = k_avg_df.combine(k_rank_df, arbitrary_func)
    k_df = k_df.combine(k_total_df, arbitrary_func)
    k_df = k_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )

    # assign strength of schedule
    playoff_sos = []
    season_sos = []
    full_sos = []
    boom = []
    bust = []
    starter = []
    ppr_boom = []
    ppr_bust = []
    ppr_starter = []
    for index, row in k_df.iterrows():
        player_positions[index] = "K"
        if row["TEAM"] == "FA":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]]["K"])
            season_sos.append(season[row["TEAM"]]["K"])
            full_sos.append(full[row["TEAM"]]["K"])

        if index in all_boom_bust:
            boom.append(all_boom_bust[index]["BOOM"])
            bust.append(all_boom_bust[index]["BUST"])
            starter.append(all_boom_bust[index]["STARTER"])
            ppr_boom.append(all_boom_bust[index]["PPR_BOOM"])
            ppr_bust.append(all_boom_bust[index]["PPR_BUST"])
            ppr_starter.append(all_boom_bust[index]["PPR_STARTER"])
        else:
            boom.append(0)
            bust.append(0)
            starter.append(0)
            ppr_boom.append(0)
            ppr_bust.append(0)
            ppr_starter.append(0)

    k_df["FULL_SOS"] = full_sos
    k_df["SEASON_SOS"] = season_sos
    k_df["PLAYOFF_SOS"] = playoff_sos
    k_df["BOOM"] = boom
    k_df["BUST"] = bust
    k_df["STARTER"] = starter
    k_df["PPR_BOOM"] = ppr_boom
    k_df["PPR_BUST"] = ppr_bust
    k_df["PPR_STARTER"] = ppr_starter
    k_df.to_csv("final/ks.csv")

    # Now we'll do all
    all_ppr_avg_df = pd.read_csv("all_ppr_avg_stats.csv")
    all_ppr_avg_df.set_index("PLAYER NAME", inplace=True)

    all_avg_df = pd.read_csv("all_avg_stats.csv")
    all_avg_df.set_index("PLAYER NAME", inplace=True)

    all_ppr_rank_df = pd.read_csv("all_ppr_rank_stats.csv")
    all_ppr_rank_df.set_index("PLAYER NAME", inplace=True)

    all_ppr_total_df = pd.read_csv("all_ppr_total_stats.csv")
    all_ppr_total_df.set_index("PLAYER NAME", inplace=True)

    all_rank_df = pd.read_csv("all_rank_stats.csv")
    all_rank_df.set_index("PLAYER NAME", inplace=True)

    all_total_df = pd.read_csv("all_total_stats.csv")
    all_total_df.set_index("PLAYER NAME", inplace=True)

    all_df = all_avg_df.combine(all_ppr_avg_df, arbitrary_func)
    all_df = all_df.combine(all_ppr_total_df, arbitrary_func)
    all_df = all_df.combine(all_total_df, arbitrary_func)
    all_df = all_df.drop(["PPR_RK", "PPR_TIERS", "TEAM"], axis=1)
    all_df = all_df.combine(all_rank_df, arbitrary_func)
    all_df = all_df.combine(all_ppr_rank_df, arbitrary_func)
    all_df = all_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "PPR_AVG.": "PPR_AVG_RK",
            "PPR_BEST": "PPR_BEST_RK",
            "PPR_STD.DEV": "PPR_STD.DEV_RK",
            "PPR_WORST": "PPR_WORST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )
    all_df = all_df.dropna(subset=["TEAM"])

    # assign strength of schedule and position
    position = []
    playoff_sos = []
    season_sos = []
    full_sos = []
    depth = []

    for index, row in all_df.iterrows():
        name = index
        pos = "UNKNOWN"
        if name in player_positions:
            pos = player_positions[name]

        position.append(pos)

        if row["TEAM"] == "FA" or pos == "UNKNOWN":
            playoff_sos.append(33)
            season_sos.append(33)
            full_sos.append(33)
        else:
            playoff_sos.append(playoff[row["TEAM"]][pos])
            season_sos.append(season[row["TEAM"]][pos])
            full_sos.append(full[row["TEAM"]][pos])

        if index in depth_chart:
            depth.append(depth_chart[index]["DEPTH"])
        else:
            depth.append(0)

    # all_df['POS'] = position
    all_df.insert(0, "POS", position)
    all_df["FULL_SOS"] = full_sos
    all_df["SEASON_SOS"] = season_sos
    all_df["PLAYOFF_SOS"] = playoff_sos
    all_df["DEPTH"] = depth
    all_df.to_csv("final/all_positions.csv")

    # For the master sheet, we'll combine all of the dataframes, keeping any rows with unique indices and combining the rest
    master_dictionary = all_df.to_dict("index")
    positional_dictionaries = [
        qb_df.to_dict("index"),
        rb_df.to_dict("index"),
        wr_df.to_dict("index"),
        te_df.to_dict("index"),
        def_df.to_dict("index"),
        k_df.to_dict("index"),
    ]

    for pos_dict in positional_dictionaries:
        for key, value in pos_dict.items():
            if key not in master_dictionary:
                master_dictionary[key] = value
            else:
                for k, v in value.items():
                    if (
                        k not in master_dictionary[key]
                        or master_dictionary[key][k] == ""
                        or pd.isnull(master_dictionary[key][k])
                    ):
                        master_dictionary[key][k] = v
            master_dictionary[key]["POS"] = player_positions[key]

    master_df = pd.DataFrame.from_dict(master_dictionary, orient="index")
    # set the index column name to PLAYER NAME
    master_df.index.name = "PLAYER NAME"

    # master_df.to_csv('after.csv')
    # master_df = all_df.combine(qb_df, arbitrary_func)
    # master_df = master_df.combine(rb_df, arbitrary_func)
    # master_df = master_df.combine(wr_df, arbitrary_func)
    # master_df = master_df.combine(te_df, arbitrary_func)
    # master_df = master_df.combine(def_df, arbitrary_func)
    # master_df = master_df.combine(k_df, arbitrary_func)
    master_df = master_df.rename(
        columns={
            "AVG.": "AVG_RK",
            "BEST": "BEST_RK",
            "PPR_AVG.": "PPR_AVG_RK",
            "PPR_BEST": "PPR_BEST_RK",
            "PPR_STD.DEV": "PPR_STD.DEV_RK",
            "PPR_WORST": "PPR_WORST_RK",
            "STD.DEV": "STD.DEV_RK",
            "WORST": "WORST_RK",
        }
    )
    master_df = master_df[~master_df.index.duplicated(keep="first")]
    master_df.to_csv("final/master_sheet.csv")


if __name__ == "__main__":
    main()
