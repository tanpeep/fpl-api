from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
import json


def general_apicall(request):
    response = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
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
def teams_api(request):
    team_name = request.data.get('team')

    data = general_apicall(request)

    if data is not None :
        response = ''

        if team_name == "all" :
            response = data["teams"]
        else :
            for team in data["teams"] :
                if team["name"] == team_name :
                    response = team
                    break

            if response == '':
                response = {'status' : "Premier League team name mismatch"}

        return Response(data=response)
    else :
        return Response(data={'status' : status.HTTP_400_BAD_REQUEST})
    
@api_view(['GET'])
def events_api(request):
    gameweek = request.data.get('gameweek')

    data = general_apicall(request)

    if data is not None :
        response = ''

        if gameweek == "all" :
            response = data["events"]
        else :
            for event in data["events"] :
                if event["name"] == "Gameweek " + gameweek :
                    response = event
                    break

            if response == '':
                response = {'status' : "Gameweek mismatch"}

        return Response(data=response)
    else :
        return Response(data={'status' : status.HTTP_400_BAD_REQUEST})
    
@api_view(['GET'])
def settings_rules_api(request):
    data = general_apicall(request)

    if data is not None :
        response = data['game_settings']

        return Response(data=response)
    else :
        return Response(data={'status' : status.HTTP_400_BAD_REQUEST})


@api_view(['GET'])
def players_api(request):
    player_name = request.data.get('player')

    data = general_apicall(request)

    if data is not None :
        response = []

        if player_name == "all" :
            response = data["elements"]
        else :
            for player in data["elements"] :
                if player["first_name"] + " " + player["second_name"] == player_name or player["first_name"] == player_name or player["second_name"] == player_name:
                    response.append(player)

            if response == []:
                response = {'status' : "Player name mismatch"}

        return Response(data=response)
    else :
        return Response(data={'status' : status.HTTP_400_BAD_REQUEST})


