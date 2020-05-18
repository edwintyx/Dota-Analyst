import boto3
import csv
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

folder = "ML-Data"
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def update_db_predictions_table():
    table = dynamodb.Table('DotaMatchPredictions')

    # read csv
    with open(folder + "/predictions.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            MatchID = row['MatchID']
            Team1 = row['Team1']
            Team2 = row['Team2']
            Predictions = row['Predictions']
            p_0 = row['p_0']
            p_1 = row['p_1']

            table.put_item(
                Item = {
                    'MatchID': MatchID,
                    'Team1': Team1,
                    'Team2': Team2,
                    'Predictions': Predictions,
                    'p_0': p_0,
                    'p_1': p_1
                }
            )

def read_db_predictions_table(MatchID):
    print(f"Receive ID: {MatchID}")
    table = dynamodb.Table('DotaMatchPredictions')
    try:
        response = table.get_item(
            Key={
                'MatchID': MatchID
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
    return item
        
