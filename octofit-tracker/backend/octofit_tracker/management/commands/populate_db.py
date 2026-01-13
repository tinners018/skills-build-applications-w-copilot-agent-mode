from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

# Define models for teams, activities, leaderboard, and workouts
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    suggested_for = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (superheroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
        ]
        for u in users:
            User.objects.create_user(username=u['username'], email=u['email'], password='password')

        # Create activities
        Activity.objects.create(user='ironman', activity_type='Running', duration=30, team='Marvel')
        Activity.objects.create(user='batman', activity_type='Cycling', duration=45, team='DC')
        Activity.objects.create(user='spiderman', activity_type='Swimming', duration=25, team='Marvel')
        Activity.objects.create(user='superman', activity_type='Flying', duration=60, team='DC')

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=100)
        Leaderboard.objects.create(team='DC', points=90)

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity for heroes', suggested_for='Marvel')
        Workout.objects.create(name='Power Circuit', description='Strength and stamina', suggested_for='DC')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
