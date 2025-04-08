from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts
from bson.objectid import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        users = [
            User(_id=ObjectId(), username=user['username'], email=user['email'], password=user['password'])
            for user in test_users
        ]
        User.objects.bulk_create(users)

        # Create teams
        teams = []
        for team in test_teams:
            team_obj = Team(_id=ObjectId(), name=team['name'])
            team_obj.save()
            team_obj.members = list(User.objects.filter(username__in=team['members']))
            team_obj.save()
            teams.append(team_obj)

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=User.objects.get(username=activity['user']),
                     activity_type=activity['activity_type'], duration=timedelta(hours=int(activity['duration'].split(':')[0]),
                                                                              minutes=int(activity['duration'].split(':')[1])))
            for activity in test_activities
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=User.objects.get(username=entry['user']), score=entry['score'])
            for entry in test_leaderboard
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name=workout['name'], description=workout['description'])
            for workout in test_workouts
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
