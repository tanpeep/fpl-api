from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
import json

from .views_general import general_apicall


def fixtures_apicall(request):
    response = requests.get('https://fantasy.premierleague.com/api/fixtures/')
    if response.status_code == 200:
        data = response.json()
        print('Success retrieve data')

        # decoder = json.JSONDecoder()
        # data = decoder.decode(api_response_json, Fpl)
        # data = json.loads(api_response_json.text)

        print(data)
        return data
    else:
        print('Failed to retrieve data from API')
        return None
    
@api_view(['GET'])
def fixtures_api(request):
    gameweek = request.data.get('gameweek')

    data = fixtures_apicall(request)
    general_data = general_apicall(request)

    if data is not None :
        response = []

        if gameweek == "all" :
            response = data
        else :
            for match in data :
                if check_event(match["event"], general_data) == "Gameweek " + gameweek :
                    response.append(match)

            if response == []:
                response = {'status' : "Gameweek mismatch"}

        for i in range(len(response)):
            response[i]['event'] = check_event(response[i]['event'], general_data)

            home_team_name = check_club_name(response[i]['team_h'], general_data)
            response[i]['team_h'] = home_team_name

            away_team_name = check_club_name(response[i]['team_a'], general_data)
            response[i]['team_a'] = away_team_name

            for j in range(len(response[i]["stats"])):
                for k in range(len(response[i]["stats"][j]['a'])):
                    response[i]["stats"][j]['a'][k]['element'] = check_player(response[i]["stats"][j]['a'][k]['element'], general_data)


        return Response(data=response)
    else :
        return Response(data={'status' : status.HTTP_400_BAD_REQUEST})
    

def check_event(id, data):
    for event in data["events"]:
        if event["id"] == id:
            return event["name"]
        
def check_club_name(id, data):
    for team in data["teams"]:
        if team["id"] == id:
            return team["name"]
        
def check_player(id, data):
    for player in data["elements"] :
        if player["id"] == id :
            return player["first_name"] + " " + player["second_name"]
