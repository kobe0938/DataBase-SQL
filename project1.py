# Collaborators: Fill in names and SUNetIDs here

def query_one():
    """Query for Stanford's venue"""
    return """
      SELECT
      venue_name,
      venue_capacity
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_teams`
      WHERE
      market = 'Stanford'
    """

def query_two():
    """Query for games in Stanford's venue"""
    return """
      SELECT
      COUNT(DISTINCT game_id) AS games_at_maples_pavilion
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`
      WHERE
      season = 2013
      AND venue_name = 'Maples Pavilion'
    """

def query_three():
    """Query for maximum-red-intensity teams"""
    return """
      SELECT
      market,
      color
      FROM
      `bigquery-public-data.ncaa_basketball.team_colors`
      WHERE
      LOWER(color) LIKE '#ff%'
      ORDER BY
      market
    """

def query_four():
    """Query for Stanford's wins at home"""
    return """
      SELECT
      COUNT(DISTINCT game_id) AS number,
      ROUND(AVG(points_game), 2) AS avg_stanford,
      ROUND(AVG(opp_points_game), 2) AS avg_opponent
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`
      WHERE
      market = 'Stanford'
      AND home_team = TRUE
      AND win = TRUE
      AND season BETWEEN 2013 AND 2017
    """

def query_five():
    """Query for players for birth city"""
    return """
      SELECT
      COUNT(DISTINCT players_games.player_id) AS num_players
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_players_games_sr` players_games
      JOIN
      `bigquery-public-data.ncaa_basketball.mbb_teams` teams
      ON
      players_games.team_market = teams.market
      WHERE
      players_games.birthplace_city = teams.venue_city
      AND players_games.birthplace_state = teams.venue_state
    """

def query_six():
    """Query for biggest blowout"""
    return """
      SELECT
      win_name, lose_name, win_pts, lose_pts, (win_pts - lose_pts) AS margin 
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games` 
      ORDER BY 
      margin DESC LIMIT 1
    """

def query_seven():
    """Query for historical upset percentage"""
    return """
      SELECT
      ROUND( 100 * COUNT(*)/(
         SELECT
            COUNT(*)
         FROM
            `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games` ), 2) AS upset_percentage
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_historical_tournament_games`
      WHERE
      win_seed > lose_seed
    """

def query_eight():
    """Query for teams with same states and colors"""
    return """
      SELECT DISTINCT name1, name2, venue_state 
      FROM((SELECT teams.name AS name1,teams2.name AS name2, teams2.venue_state, teams.market AS market1, teams2.market AS market2 FROM `bigquery-public-data.ncaa_basketball.mbb_teams` teams
      JOIN `bigquery-public-data.ncaa_basketball.mbb_teams` teams2
      ON teams2.venue_state = teams.venue_state
      WHERE teams.market != teams2.market
      ) teams3
      JOIN 
      (SELECT color.market AS market3,color2.market AS market4 FROM `bigquery-public-data.ncaa_basketball.team_colors` color
      JOIN `bigquery-public-data.ncaa_basketball.team_colors` color2
      ON color.color = color2.color
      WHERE color.market != color2.market
      ) color3
      ON teams3.market1 = color3.market3
      AND teams3.market2 = color3.market4 )
      WHERE name2 >= name1
      ORDER BY name1
    """

def query_nine():
    """Query for top geographical locations"""
    return """
      SELECT
      birthplace_city,
      birthplace_state,
      birthplace_country,
      SUM(points)
      FROM
      `bigquery-public-data.ncaa_basketball.mbb_players_games_sr`
      WHERE
      team_market = 'Stanford'
      AND season BETWEEN 2013
      AND 2017
      GROUP BY
      birthplace_city,
      birthplace_state,
      birthplace_country
      ORDER BY
      SUM(points) DESC
      LIMIT
      3
    """

def query_ten():
    """Query for teams with lots of high-scorers"""
    return """
      SELECT
      team_market,
      COUNT(*) AS num_players
      FROM (
      SELECT
         DISTINCT player_id,
         team_market
      FROM
         `bigquery-public-data.ncaa_basketball.mbb_pbp_sr`
      WHERE
         period = 1
         AND season >= 2013
      GROUP BY
         game_id,
         player_id,
         team_market
      HAVING
         SUM(points_scored) >= 15)
      GROUP BY
      team_market
      HAVING
      COUNT(*) > 5
      ORDER BY
      COUNT(*) DESC,
      team_market
      LIMIT
      5
    """

def query_eleven():
    """Query for highest-winner teams"""
    return """
      SELECT
        his.market,
        COUNT(*) AS times
      FROM ( (
          SELECT
            season,
            MAX(wins) AS top_times
          FROM
            `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons`
          WHERE
            season BETWEEN 1900
            AND 2000
          GROUP BY
            season) top
        JOIN
          `bigquery-public-data.ncaa_basketball.mbb_historical_teams_seasons` his
        ON
          top.top_times = his.wins
          AND top.season = his.season )
      WHERE
        his.market IS NOT NULL
      GROUP BY
        his.market
      ORDER BY
        times DESC
      LIMIT
        5
    """