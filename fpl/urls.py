from django.urls import path
from .views import views_general, views_fixtures

urlpatterns = [
    path('teams', views_general.teams_api, name="teams api"),
    path('events', views_general.events_api, name="events api"),
    path('settings-rules', views_general.settings_rules_api, name="settings rules api"),
    path('players', views_general.players_api, name="players api"),
    path('fixtures',  views_fixtures.fixtures_api, name="fixtures api")
]