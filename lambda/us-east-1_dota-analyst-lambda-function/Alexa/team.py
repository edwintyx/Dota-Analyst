from liquipediapy import dota
import requests
import re

def create_team_overview_message(team_id, team_name):
    dota_obj = dota("alexa-skill-dota-analyst-final-project(eytan1@sheffield.ac.uk)")
    team_details = dota_obj.get_team_info(team_id,False)
    # Team location
    team_location = team_details['info']['location'][0]
    # Active players
    team_roster_one_ID = team_details['team_roster'][0]['ID']
    team_roster_two_ID = team_details['team_roster'][1]['ID']
    team_roster_three_ID = team_details['team_roster'][2]['ID']
    team_roster_four_ID = team_details['team_roster'][3]['ID']
    team_roster_five_ID = team_details['team_roster'][4]['ID']
    # Achievements List
    achievements_list = team_details['cups']
    achievements_length = len(achievements_list)
    # Format String
    message = f"Here is a short overview of {team_name}." \
        f" The team is currently located in {team_location}." \
        f" Their current active players are," \
        f" {team_roster_one_ID}," \
        f" {team_roster_two_ID}," \
        f" {team_roster_three_ID}," \
        f" {team_roster_four_ID}," \
        f" and {team_roster_five_ID}." \
        f" Overall the team has won a total of {achievements_length} major tournaments."
    return message

def create_team_achievements_message(team_id, team_name):
    dota_obj = dota("alexa-skill-dota-analyst-final-project(eytan1@sheffield.ac.uk)")
    team_details = dota_obj.get_team_info(team_id,False)
    achievements_list = team_details['cups']
    #re_achievements = re.sub('[^A-Za-z0-9]+', ' ', str(achievements_list))
    achievements_length = len(achievements_list)
    create_achievement_list = ""

    if achievements_length > 0:
        for i in range(achievements_length):
            create_achievement_list += f"{i+1}, {achievements_list[i]}, "
        message = f"Here are a list of {team_name} achievements. " \
                  f"{create_achievement_list}"
    else:
        create_achievement_list = "None"
        message = f"Unfortunately {team_name} has no achievements. "
    return message

def create_team_roster_message(team_id, team_name):
    dota_obj = dota("alexa-skill-dota-analyst-final-project(eytan1@sheffield.ac.uk)")
    team_details = dota_obj.get_team_info(team_id,False)

    team_roster_one_ID = team_details['team_roster'][0]['ID']
    team_roster_one_POS = team_details['team_roster'][0]['Position']
    if '/' in team_roster_one_POS:
        team_roster_one_POS = team_roster_one_POS.replace('/'," or ")
    if 'Position:' in team_roster_one_POS:
        team_roster_one_POS = team_roster_one_POS.replace('Position:',"")
        
    team_roster_two_ID = team_details['team_roster'][1]['ID']
    team_roster_two_POS = team_details['team_roster'][1]['Position']
    if '/' in team_roster_two_POS:
        team_roster_two_POS = team_roster_two_POS.replace('/'," or ")
    if 'Position:' in team_roster_two_POS:
        team_roster_two_POS = team_roster_two_POS.replace('Position:',"")
        
    team_roster_three_ID = team_details['team_roster'][2]['ID']
    team_roster_three_POS = team_details['team_roster'][2]['Position']
    if '/' in team_roster_three_POS:
        team_roster_three_POS = team_roster_three_POS.replace('/'," or ")
    if 'Position:' in team_roster_three_POS:
        team_roster_three_POS = team_roster_three_POS.replace('Position:',"")
        
    team_roster_four_ID = team_details['team_roster'][3]['ID']
    team_roster_four_POS = team_details['team_roster'][3]['Position']
    if '/' in team_roster_four_POS:
        team_roster_four_POS = team_roster_four_POS.replace('/'," or ")
    if 'Position:' in team_roster_four_POS:
        team_roster_four_POS = team_roster_four_POS.replace('Position:',"")
        
    team_roster_five_ID = team_details['team_roster'][4]['ID']
    team_roster_five_POS = team_details['team_roster'][4]['Position']
    if '/' in team_roster_five_POS:
        team_roster_five_POS = team_roster_five_POS.replace('/'," or ")
    if 'Position:' in team_roster_five_POS:
        team_roster_five_POS = team_roster_five_POS.replace('Position:',"")
    
    message = f"Here are the rosters for {team_name}. " \
            f" {team_roster_one_ID}, will be playing as position {team_roster_one_POS} (Hard-Carry)." \
            f" {team_roster_two_ID}, as position {team_roster_two_POS} (Semi-Carry)." \
            f" {team_roster_three_ID}, as position {team_roster_three_POS} (Offlaner)." \
            f" {team_roster_four_ID}, as position {team_roster_four_POS} (Roaming Support), and" \
            f" {team_roster_five_ID}, as position {team_roster_five_POS} (Hard Support)."
    return message

def create_team_match_results_message(team_id, team_name):
    opendota_match_list = get_opendota_teams_matches(team_id)
    updated_match_list = update_opendota_team_matches(opendota_match_list)
    match_list_length = len(updated_match_list)
    create_speech = ""
    for i in range(match_list_length):
        tournament = updated_match_list[i]['league_name']
        team2 = updated_match_list[i]['opposing_team_name']
        results = updated_match_list[i]['results']
        create_speech += f"Match {i+1}. {tournament}. '{team_name}' {results} against '{team2}'. "
    message = f"Here are the results of 5 most recent games played by {team_name}. {create_speech}"
    return message

def get_opendota_teams_matches(team_id):
    url = f"https://api.opendota.com/api/teams/{team_id}/matches"
    print(url)
    page = requests.get(url)
    data = page.json()
    match_list = []
    for i in range(0,5):
        match_list.append(data[i])
        # Extract 10 matches and put in match_list, List of dictionaries
        # message = f"{i+1}\n{data[i]}\n\n"
    #print("-- Extracted Match List --\n",match_list)
    return match_list

def update_opendota_team_matches(extracted_matches_list):
    for items in extracted_matches_list:
        items.pop('start_time')
        items.pop('leagueid')
        items.pop('cluster')
        items.pop('opposing_team_logo')
        duration = items['duration']
        minutes, seconds = divmod(duration, 60)   
        final_duration = str('{} minutes, {} seconds'.format(int(minutes), int(seconds)))
        items.update({'duration':final_duration})
        if items['radiant_win'] == True and items['radiant'] == True:
            items.update({'results':'Won Match'})
        elif items['radiant_win'] == False and items['radiant'] == False:
            items.update({'results':'Won'})
        else: 
            items.update({'results':'Lost'})
    return extracted_matches_list