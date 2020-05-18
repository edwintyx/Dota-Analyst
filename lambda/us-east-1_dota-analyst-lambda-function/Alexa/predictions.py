import pandas as pd
import math
import csv

def build_team_dict():
    folder = "ML-Data"
    team_ids = pd.read_csv(folder + '/Teams.csv')
    team_id_map = {}
    for index, row in team_ids.iterrows():
        team_id_map[row['Team_Id']] = row['Team_Name']
    return team_id_map

def create_team_prediction_response(predict_dict):
    prediction_dict = predict_dict
    team_id_map = build_team_dict()
    team1 = prediction_dict['Team1']
    team2 = prediction_dict['Team2']
    prediction_result = int(prediction_dict['Predictions'])
    prediction_probability_win = round(float(prediction_dict['p_1']) * 100, 2)
    prediction_probability_lose = round(float(prediction_dict['p_0']) * 100, 2)
    
    if prediction_result == 1:
        winning_team = int(team1)
        losing_team = int(team2)
        winning = team_id_map[winning_team]
        losing = team_id_map[losing_team]
        message = f"According to the prediction model, {winning} will win {losing} with a probability of {prediction_probability_win} percent."
    else:
        winning_team = int(team2)
        losing_team = int(team1)
        winning = team_id_map[winning_team]
        losing = team_id_map[losing_team]
        message = f"Unfortunately, according to the prediction model, {losing} will lose to {winning} with a probability of {prediction_probability_lose} percent."
    return message