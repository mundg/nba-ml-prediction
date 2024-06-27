from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, leaguegamefinder 
from nba_api.live.nba.endpoints import boxscore

import pandas as pd


def get_advanceStats(number_id:str) -> pd.DataFrame:
    # Blank Dictionary
    team_info = {'gameId': '', 'attendance': 0, 'home_teamID':0, 'away_teamID':0}
    # Call API 
    data = boxscore.BoxScore(game_id=number_id).game.get_dict()
    # Store Values
    home_stats = {f'home_{key}':value for key,value in data['homeTeam']['statistics'].items()}
    away_stats = {f'away_{key}':value for key,value in data['awayTeam']['statistics'].items()}
    team_info['gameId'] = data['gameId']
    team_info['attendance'] = data['attendance']
    team_info['home_teamID'] = data['homeTeam']['teamId']
    team_info['away_teamID'] = data['awayTeam']['teamId']

    # Combine 
    final_dict = {**home_stats, **away_stats, **team_info}
    return pd.DataFrame([final_dict])

def main():
    df_team_stats = (leaguegamefinder.LeagueGameFinder()).get_data_frames()[0]
    df_team_names = pd.DataFrame(teams.get_teams())
    
    n = 10
    final_df = df_team_stats.loc[ (df_team_stats['TEAM_NAME'].isin([*list(df_team_names['full_name'].unique())] + ['LA Clippers'])) & (df_team_stats['GAME_DATE'] >= '2023-11-24'), :][:n]

    dataframes_list = []
    missing_game_ids = []
    
    for game_id in final_df['GAME_ID'].unique():
        try:
            dataframe = get_advanceStats(game_id)
            dataframes_list.append(dataframe)
        except Exception as e:
            print(e)
            missing_game_ids.append(game_id)

    combined_df = pd.concat(dataframes_list, axis=0)   
    combined_df.to_csv('data/nba_stats.csv') 


if __name__ == '__main__':
    print('Initializing...')
    main()
    