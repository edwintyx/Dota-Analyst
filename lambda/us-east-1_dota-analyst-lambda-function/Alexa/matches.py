from liquipediapy import dota
from datetime import datetime
from datetime import timedelta
import re

def create_ongoing_match_message():
    updated_matches_list = get_updated_matches()
    matches_list = get_live_matches_list(updated_matches_list)
    list_length = len(matches_list)
    create_speech = ""
    if list_length > 0:
        for i in range(list_length):
            team1 = matches_list[i]['team1']
            match_format = matches_list[i]['format']
            team2 = matches_list[i]['team2']
            tournament = matches_list[i]['tournament']
            re_tournament = re.sub('[^A-Za-z0-9]+', ' ', str(tournament))
            create_speech += f" Match {i+1}, '{team1}' versus '{team2}'. {match_format}. Tournament is {re_tournament}."
        if list_length == 1:
            message = f"There are currently {list_length} ongoing match happening right now. {create_speech}"
        else:
            message = f"There are currently {list_length} ongoing matches happening right now. {create_speech}"
    else:
        message = "Sorry, there are currently no ongoing matches happening right now. Try requesting for upcoming matches instead."
    return message

def create_upcoming_match_message(start, end):
    updated_matches_list = get_updated_matches()
    matches_list = get_upcoming_matches_list(updated_matches_list)
    list_length = len(matches_list)
    create_speech = ""
    if list_length > 0:
        for i in range(start, end):
            team1 = matches_list[i]['team1']
            match_format = matches_list[i]['format']
            team2 = matches_list[i]['team2']
            start_time = matches_list[i]['start_time']
            tournament = matches_list[i]['tournament']
            re_tournament = re.sub('[^A-Za-z0-9]+', ' ', str(tournament))
            create_speech += f" Match {i+1}, '{team1}' versus '{team2}', at {start_time}. {match_format}. Tournament is {re_tournament}."
        message = f"{create_speech}"
    else:
        message = "Sorry, there are currently no upcoming matches. "
    return message

def create_match_status_summary_message(match_value):
    match_length = int(match_value)
    updated_matches_list = get_updated_matches()
    matches_list = get_upcoming_matches_list(updated_matches_list)
    list_length = len(matches_list)
    create_speech = ""
    if list_length > 0:
        for i in range(0, match_length):
            team1 = matches_list[i]['team1']
            team2 = matches_list[i]['team2']
            status = matches_list[i]['status']
            if i == match_length - 1:
                create_speech += f" and Match {i+1}, '{team1}' versus '{team2}' will start in {status} from now."
            else:
                create_speech += f" Match {i+1}, '{team1}' versus '{team2}' will start in {status} from now."
        message = f"Here is a summary of match status. {create_speech}"
    else:
        message = "Sorry, there are currently no match status summary. "
    return message


def get_live_matches_list(match_list):
    live_match_list = []
    for item in match_list:
         if item['status'] == 'Live!':
           live_match_list.append(item)
    return live_match_list

def get_upcoming_matches_list(match_list):
    upcoming_match_list = []
    for item in match_list:
         if item['status'] != 'Live!':
           upcoming_match_list.append(item)
    return upcoming_match_list

def get_updated_matches():
    dota_obj = dota("alexa-skill-dota-analyst-final-project(eytan1@sheffield.ac.uk)")
    games = dota_obj.get_upcoming_and_ongoing_games()
    get_match_list = games
    for items in get_match_list:
        items.pop('twitch_channel')
        if items['format'] == 'Bo1':
            items.update({'format':'Best of 1'})
        elif items['format'] == 'Bo2':
            items.update({'format':'Best of 2'})
        elif items['format'] == 'Bo3':
            items.update({'format':'Best of 3'})
        else: 
            items.update({'format':'Best of 5'})
        match_time = items['start_time']
        converted_match_time = format_match_time(match_time)
        remaining_time_result = add_match_status(match_time)
        items.update({'start_time':converted_match_time})
        items.update({'status':remaining_time_result})
    return get_match_list

def format_match_time(match_time):
    start_time_obj = datetime.strptime(match_time, "%B %d, %Y - %H:%M UTC")
    get_new_time = start_time_obj + timedelta(minutes = 60)
    new_time = get_new_time.strftime('%d-%b-%Y %I:%M %p')
    return new_time

def add_match_status(get_time):
    start_time = datetime.strptime(get_time, "%B %d, %Y - %H:%M UTC")
    now_time = datetime.now()
    remaining_time = start_time - now_time
    remaining_time_in_secs = remaining_time.total_seconds()
    if remaining_time_in_secs > 0:
        days, remainder_days = divmod(remaining_time_in_secs, 86400)
        hours, remainder_hours = divmod(remainder_days, 3600)
        minutes, seconds = divmod(remainder_hours, 60)   
        if days > 0:
            remaining_time_result = str('{} days {} hours {} minutes'.format(int(days), int(hours), int(minutes)))
        elif hours > 0:
            remaining_time_result = str('{} hours {} minutes'.format(int(hours), int(minutes)))
        elif minutes > 0:
            remaining_time_result = str('{}minutes {} seconds'.format(int(minutes), int(seconds)))
        else:
            remaining_time_result = str('{} seconds'.format(int(seconds)))
    else:
        remaining_time_result = "Live!"
    return remaining_time_result