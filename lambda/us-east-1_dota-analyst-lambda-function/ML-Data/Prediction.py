"""
This tool
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report,confusion_matrix
#from sklearn import cross_validation, linear_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import csv


base_elo = 2000
team_elos = {}  
team_stats = {}
X = []
y = []
submission_data = []
prediction_year = 2019


def initialize_data():
    for i in range(2018, 2020):
        team_elos[i] = {}
        team_stats[i] = {}


def predict_winner(team_1, team_2, model, season, stat_fields):
    features = []

    # Team 1
    for stat in stat_fields:
        features.append(get_stat(season, team_1, stat))

    # Team 2
    for stat in stat_fields:
        features.append(get_stat(season, team_2, stat))

    return model.predict_proba([features])

def predict_Y_winner(team_1, team_2, model, season, stat_fields):
    features = []

    # Team 1
    for stat in stat_fields:
        features.append(get_stat(season, team_1, stat))

    # Team 2
    for stat in stat_fields:
        features.append(get_stat(season, team_2, stat))

    return model.predict([features])


def update_stats(season, team, fields):
    if team not in team_stats[season]:
        team_stats[season][team] = {}

    for key, value in fields.items():
        if key not in team_stats[season][team]:
            team_stats[season][team][key] = []
   
        team_stats[season][team][key].append(value)


def get_stat(season, team, field):
    try:
        l = team_stats[season][team][field]
        return sum(l) / float(len(l))
    except:
        return 0


def build_team_dict():
    team_ids = pd.read_csv('Teams.csv')
    team_id_map = {}
    for index, row in team_ids.iterrows():
        team_id_map[row['Team_Id']] = row['Team_Name']
    return team_id_map

def build_season_data(all_data):
    print("Building season data.")
    for index, row in all_data.iterrows():
 
        team_1_features = []
        team_2_features = []
        
        for field in stat_fields:
            # winning team 
            team_1_stat = row['r_'+ field]
            # losing team
            team_2_stat = row['d_' + field]
            team_1_features.append(team_1_stat)
            team_2_features.append(team_2_stat)
            
        X.append(team_1_features + team_2_features)
        
        if row['r_winner'] == 1:
            y.append(1)
        else:
            y.append(0)
            
            # [ match_id, start_time, Wteam, Wscore, Lteam, Lscore,
            #   kills, deaths, assists,
            #   last_hits, denies,
            #   hero_damage, tower_damage, hero_healing
            #   xp_per_min, gold_per_min ]

        stat_1_fields = {}
        stat_2_fields = {}

        for stat in stat_fields:
            #if row['r_winner'] == 1 and row['match_id'] <= 4875804229:
            if row['r_winner'] == 1:
                if stat == 'score':
                    # stat1 = winner
                    stat_1_fields['score'] = row['r_score']
                    # stat2 = loser
                    stat_2_fields['score'] = row['d_score']
                else:
                    stat_1_fields[stat] = row['r_' + stat]
                    stat_2_fields[stat] = row['d_' + stat]
            else:
                if stat == 'score':
                    # stat1 = winner
                    stat_1_fields['score'] = row['d_score']
                    # stat2 = loser
                    stat_2_fields['score'] = row['r_score']
                else:
                    stat_1_fields[stat] = row['d_' + stat]
                    stat_2_fields[stat] = row['r_' + stat]

        update_stats(row['Season'], row['Wteam'], stat_1_fields)
        update_stats(row['Season'], row['Lteam'], stat_2_fields)


    return X, y

if __name__ == "__main__":
    
    team_ids = []
    team_names = []
    prediction_list = []

    stat_fields = ['score','kills','assists','dmg','lasthits','denies','gpm','xpm']

    initialize_data()
    all_data = pd.read_csv('test.csv')
    X, y = build_season_data(all_data)
    
    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
    
    
    model = LogisticRegression(solver = 'lbfgs', random_state = 0)
    # logistic regression
    logmodel = LogisticRegression()
    #svc_model = SVC()
    #KNN = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    
    
    # Fit the model.
    print("Fitting on %d samples." % len(X_train))
    
    #model = LogisticRegression()

    # Check accuracy.
    print("Doing cross-validation.")
    print(cross_val_score(model, X_train, y_train, cv=10, scoring='accuracy', n_jobs=-1).mean())
    print("logmodel accuracy: ",cross_val_score(logmodel, X_train, y_train, cv=10, scoring='accuracy', n_jobs=-1).mean())
    #print("svc_model accuracy: ",cross_val_score(svc_model, X_train, y_train, cv=10, scoring='accuracy', n_jobs=-1).mean())
    #print("KNN_model accuracy: ",cross_val_score(KNN, X_train, y_train, cv=10, scoring='accuracy', n_jobs=-1).mean())
    logmodel.fit(X_train,y_train)
    predictions = logmodel.predict(X_test)
    print("logmodel_CM: ",confusion_matrix(y_test,predictions))
    
    print("Model fitting now.")
    model.fit(X_train, y_train)
    #model.fit(X, y)
    print("Model training Done")

    # Now predict tournament matchups.
    print("Getting teams.")
    seeds = pd.read_csv('TourneySeeds.csv')
    # for i in range(2016, 2017):
    tourney_teams = []
    for index, row in seeds.iterrows():
        if row['Season'] == prediction_year:
            team_name = row['Team']
            tourney_teams.append(team_name)

    # Build our prediction of every matchup.
    print("Predicting matchups.")
    tourney_teams.sort()
    for team_1 in tourney_teams:
        for team_2 in tourney_teams:
            if team_1 < team_2:
            #if team_1 != team_2:
                prediction = predict_winner(team_1, team_2, model, prediction_year, stat_fields)
                prediction_Y = predict_Y_winner(team_1, team_2, model, prediction_year, stat_fields)
                label = str(prediction_year) + '_' + str(team_1) + '_' + str(team_2)
                prediction_list.append([label, str(team_1), str(team_2), prediction_Y[0], prediction[0][0], prediction[0][1]])
               # submission_data.append([label, str(team_1), str(team_2), prediction[0][0], prediction[0][1]])
            
     # Write the results.
    print("Writing %d results." % len(prediction_list))
    with open('predictions.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['MatchID', 'Team1', 'Team2', 'Predictions', 'p_0', 'p_1'])
        writer.writerows(prediction_list)

   
    print("Outputting readable results.")
    team_id_map = build_team_dict()
    readable_test = []
    readable = []
        
    for predictions in prediction_list:
        parts_test = predictions[0].split('_')
        # Order them properly.
        if predictions[3] == 1:
            winning = int(parts_test[1])
            losing = int(parts_test[2])
            probability = predictions[5]
        else:
            winning = int(parts_test[2])
            losing = int(parts_test[1])
            probability = predictions[4]
        readable_test.append(['%s beats %s: %f' %(team_id_map[winning], team_id_map[losing], probability)])
    with open('readable_predictions.csv', 'w') as file:
        file_writer = csv.writer(file)
        file_writer.writerows(readable_test)

