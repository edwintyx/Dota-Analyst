from __future__ import print_function
import boto3
from Alexa import team
from Alexa import matches
from Alexa import predictions
from Alexa import database


dynamodb = boto3.resource('dynamodb')

# --------------- Lambda Handler function ------------------
def lambda_handler(event, context):
    #database.update_db_predictions_table()

    request = event['request']
    requestId = event['request']['requestId']
    session = event['session']
    requestType = event['request']['type']

    if event['session']['new']:
        on_session_started({'requestId': requestId}, session)

    # Routes based on request
    if requestType == "LaunchRequest":
        return on_launch(request, session)

    elif requestType == "IntentRequest":
        return on_intent(request, session)

    elif requestType == "SessionEndedRequest":
        return on_session_ended(request, session)
        

# --------------- Lambda Sessions  ------------------        

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    # print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])
    print('Starting session - Edwin')


# 
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    #print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    print('Launching Skill - without specifying any request')
    return get_welcome_response()


# Intent Logic 
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
    get_intent_values = intent_request
    get_intent_session = session
    # intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # intent_confirmation = intent_request['intent']['confirmationStatus']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetDotaTeamOverview":
        return get_team_overview_response(get_intent_values)

    elif intent_name == "GetDotaTeamAchievements":
        return get_team_achievements_response(get_intent_values)

    elif intent_name == "GetDotaTeamRoster":
        return get_team_roster_response(get_intent_values)

    elif intent_name == "GetOngoingMatches":
        return get_ongoing_matches_response()

    elif intent_name == "GetUpcomingMatches":
        return get_upcoming_matches_response()

    elif intent_name == "GetMatchStatusSummary":
        return get_match_status_summary_response(get_intent_values)

    elif intent_name == "GetDotaTeamMatchResults":
        return get_team_match_results_response(get_intent_values)

    elif intent_name == "GetDotaTeamPredictions":
        return get_team_prediction_response(get_intent_values)

    elif intent_name == "GetTIPredictions":
        return get_the_internationals_prediction_response()

    elif intent_name == "AMAZON.YesIntent":
        return get_yes_response(get_intent_session)

    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()

    elif intent_name == "AMAZON.RepeatIntent":
        return get_repeat_response(get_intent_session)

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()

    else:
        return misunderstood()

# Session Ended
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session = true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
    

# --------------- Functions that control the skill's behavior ------------------

#This is called if the app is started without a secific intent to get the workout recommendation
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello and Welcome to the Dota Analyst App. " \
                    "Ask me questions such as 'Will Team Secret win their next match? " \
                    "To find out more, ask for help."
    reprompt_text = "Ask me questions such as 'Will Team Secret win their next match? " \
                    "To find out more, ask for help."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_team_overview_response(intent_request):
    team_name = intent_request['intent']['slots']['team']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    team_id = intent_request['intent']['slots']['team']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    
    card_title = "Team Overview"
    speech_output = team.create_team_overview_message(team_id, team_name) + " Is there anything else I can help you?"
    reprompt_text = team.create_team_overview_message(team_id, team_name) + " Is there anything else I can help you?"
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_team_achievements_response(intent_request):
    team_name = intent_request['intent']['slots']['team']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    team_id = intent_request['intent']['slots']['team']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    card_title = "Team Achievements"
    speech_output = team.create_team_achievements_message(team_id, team_name) + " Is there anything else I can help you?"
    reprompt_text = team.create_team_achievements_message(team_id, team_name) + " Is there anything else I can help you?"
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_team_roster_response(intent_request):
    team_name = intent_request['intent']['slots']['team']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    team_id = intent_request['intent']['slots']['team']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    card_title = "Team Positions"
    speech_output = team.create_team_roster_message(team_id, team_name) + " Is there anything else I can help you?"
    reprompt_text = team.create_team_roster_message(team_id, team_name) + " Is there anything else I can help you?"
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_ongoing_matches_response():
    card_title = "Ongoing Matches"
    speech_output = matches.create_ongoing_match_message() + " Is there anything else I can help you?"
    reprompt_text = matches.create_ongoing_match_message() + " Is there anything else I can help you?"
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_upcoming_matches_response():
    start = 0
    end = 3
    card_title = "Upcoming Matches"
    speech_output = "Here are a list of upcoming matches." + matches.create_upcoming_match_message(start, end) + " Would you like to know more?"
    reprompt_text = "Here are a list of upcoming matches." + matches.create_upcoming_match_message(start, end) + " Would you like to know more?"
    session_attributes = {"start": 0,"end": 3,"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_match_status_summary_response(intent_request):
    match_value = intent_request['intent']['slots']['number']['value']
    card_title = "Overall Match Status"
    speech_output = matches.create_match_status_summary_message(match_value)
    reprompt_text = matches.create_match_status_summary_message(match_value)
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_team_match_results_response(intent_request):
    team_name = intent_request['intent']['slots']['teamID']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
    team_id = intent_request['intent']['slots']['teamID']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    card_title = "Team Match Results"
    speech_output = team.create_team_match_results_message(team_id, team_name)
    reprompt_text = team.create_team_match_results_message(team_id, team_name)
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_team_prediction_response(intent_request):
    team1 = intent_request['intent']['slots']['teamOneID']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    team2 = intent_request['intent']['slots']['teamTwoID']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['id']
    match_id = f"2019_{team1}_{team2}"
    prediction_dict = database.read_db_predictions_table(match_id)
    card_title = "GetDotaTeamPredictions"
    speech_output = predictions.create_team_prediction_response(prediction_dict) + " Is there anything else I can help you?"
    reprompt_text = predictions.create_team_prediction_response(prediction_dict) + " Is there anything else I can help you?"
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_the_internationals_prediction_response():
    card_title = "GetTIPredictions"
    speech_output = "According to the prediction model, Team Secret will win The Internationals 2019. Is there anything else you would like to know?"
    reprompt_text = "According to the prediction model, Team Secret will win The Internationals 2019. Is there anything else you would like to know?"
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_yes_response(intent_session):
    try:
        start = intent_session['attributes']['start'] + 3
        end = intent_session['attributes']['end'] + 3
    except KeyError:
        start = 0
        end = 0
    session_attributes = {"start": start,"end": end}
    card_title = "Yes Intent"
    if start != 0:
        speech_output = matches.create_upcoming_match_message(start, end) + " Would you like to know more?"
    else:
        speech_output = "You can ask questions like, what are the upcoming matches? or incoming matches? to find out more, ask for help."
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_repeat_response(intent_session):
    repeat_message = intent_session['attributes']['repeat_message']
    card_title = "Repeat Intent"
    speech_output = repeat_message
    reprompt_text = repeat_message
    session_attributes = {"repeat_message": speech_output}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "Here are a list of requests you may want to ask. Requests related to Dota matches. You can say, 'give me upcoming matches', 'give me ongoing matches' or\
        'Give me match status summary'. For requests regarding a Dota team. You can say, 'give me team secret overview', 'give me team secret achievements',\
            'give me team secret roster', or 'give me team secret match results'. Lastly, requests regarding predictions. You can say 'give me predictions of Team \
                Secret versus Team Liquid' or 'who do you think will win the T I'."
    reprompt_text = "Here are a list of requests you may want to ask. Requests related to Dota matches. You can say, 'give me upcoming matches', 'give me ongoing matches' or \
        'Give me match status summary'. For requests regarding a Dota team. You can say, 'give me team secret overview', 'give me team secret achievements', \
            'give me team secret roster', or 'give me team secret match results'. Lastly, requests regarding predictions. You can say 'give me predictions of Team \
                Secret versus Team Liquid' or 'who do you think will win the T I'."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
                   
      
#This is called if the request is not understood       
def misunderstood():
    session_attributes = {}
    card_title = "Misunderstood" 
    speech_output = "Sorry, I did not understand your request. " \
                    "Ask me questions such as 'When are the ongoing or upcoming matches? " \
                    "To find out more, ask for help. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I did not understand your request. " \
                    "Ask me questions such as 'What are the ongoing or upcoming matches? " \
                    "To find out more, ask for help. "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


#This is called to end the session 
def handle_session_end_request():
    session_attributes = {}
    card_title = "Session Ended"
    speech_output = "Thank you for using the Dota Analyst App. Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }