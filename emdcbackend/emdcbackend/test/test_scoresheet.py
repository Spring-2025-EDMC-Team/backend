from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Scoresheet, Teams, Judge, MapScoresheetToTeamJudge, MapClusterToTeam, MapJudgeToCluster, Contest, MapContestToTeam
from ..serializers import ScoresheetSerializer
from ..views.scoresheets_redesign import ScoresheetEnum, create_base_score_sheet_redesign

class ScoresheetRedesignTests(APITestCase):
    def setUp(self):
        # Set up test data and authentication
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create test data for teams, judges, clusters, and contests
        self.team = Teams.objects.create(name="Test Team")
        self.judge = Judge.objects.create(name="Test Judge", redesign=True)
        self.cluster = MapClusterToTeam.objects.create(teamid=self.team.id, clusterid=1)
        self.judge_cluster = MapJudgeToCluster.objects.create(judgeid=self.judge.id, clusterid=1)
        self.contest = Contest.objects.create(name="Test Contest")
        self.contest_team = MapContestToTeam.objects.create(contestid=self.contest.id, teamid=self.team.id)

        # Create a Redesign scoresheet
        self.scoresheet = Scoresheet.objects.create(
            sheetType=ScoresheetEnum.REDESIGN,
            isSubmitted=False,
            field1=0.0,  # Innovation & Creativity
            field2=0.0,  # Use of Item
            field3=0.0,  # Explanation of Solution
            field4=0.0,  # Engineering Principles
            field5=0.0,  # Learning Identification
            field6=0.0,  # Teamwork
            field7=0.0,  # Communication
            field8="junior",  # Division
            field9=""  # Comments
        )
        self.mapping = MapScoresheetToTeamJudge.objects.create(
            teamid=self.team.id,
            judgeid=self.judge.id,
            scoresheetid=self.scoresheet.id,
            sheetType=ScoresheetEnum.REDESIGN
        )

    def tearDown(self):
        # Clean up test data if needed (optional since Django rolls back the test database)
        pass

    # Test creating a Redesign scoresheet
    def test_create_score_sheet_redesign(self):
        url = reverse('create_score_sheet')  # Adjust URL name if different
        data = {
            "sheetType": ScoresheetEnum.REDESIGN,
            "isSubmitted": False,
            "innovation_creativity": 5.0,
            "use_of_item": 4.0,
            "explanation_solution": 3.0,
            "engineering_principles": 4.5,
            "learning_identification": 3.5,
            "teamwork": 4.0,
            "communication": 5.0,
            "division": "junior",
            "comments": "Great teamwork!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Scoresheet.objects.count(), 2)  # 1 from setUp, 1 from this test
        self.assertEqual(Scoresheet.objects.last().field1, 5.0)  # Innovation & Creativity
        self.assertEqual(Scoresheet.objects.last().field8, "junior")  # Division
        self.assertEqual(Scoresheet.objects.last().field9, "Great teamwork!")  # Comments

    # Test updating a Redesign scoresheet
    def test_update_scores_redesign(self):
        url = reverse('update_scores')  # Adjust URL name if different
        data = {
            "id": self.scoresheet.id,
            "sheetType": ScoresheetEnum.REDESIGN,
            "innovation_creativity": 8.0,
            "use_of_item": 7.0,
            "explanation_solution": 6.0,
            "engineering_principles": 7.5,
            "learning_identification": 6.5,
            "teamwork": 8.0,
            "communication": 9.0,
            "division": "senior",
            "comments": "Excellent redesign!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.scoresheet.refresh_from_db()
        self.assertEqual(self.scoresheet.field1, 8.0)  # Innovation & Creativity
        self.assertEqual(self.scoresheet.field7, 9.0)  # Communication
        self.assertEqual(self.scoresheet.field8, "senior")  # Division
        self.assertEqual(self.scoresheet.field9, "Excellent redesign!")  # Comments

    # Test updating a single field in a Redesign scoresheet
    def test_edit_score_sheet_field(self):
        url = reverse('edit_score_sheet_field')  # Adjust URL name if different
        data = {
            "id": self.scoresheet.id,
            "field": "field1",  # Innovation & Creativity
            "new_value": 9.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.scoresheet.refresh_from_db()
        self.assertEqual(self.scoresheet.field1, 9.0)

    # Test invalid field in edit_score_sheet_field
    def test_edit_score_sheet_field_invalid(self):
        url = reverse('edit_score_sheet_field')
        data = {
            "id": self.scoresheet.id,
            "field": "invalid_field",
            "new_value": 5.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Test retrieving a scoresheet by ID
    def test_scores_by_id(self):
        url = reverse('scores_by_id', args=[self.scoresheet.id])  # Adjust URL name if different
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["ScoreSheet"]["id"], self.scoresheet.id)
        self.assertEqual(response.data["ScoreSheet"]["sheetType"], ScoresheetEnum.REDESIGN)

    # Test deleting a Redesign scoresheet
    def test_delete_score_sheet(self):
        url = reverse('delete_score_sheet', args=[self.scoresheet.id])  # Adjust URL name if different
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Scoresheet.objects.count(), 0)
        self.assertEqual(MapScoresheetToTeamJudge.objects.count(), 0)

    # Test creating a base Redesign scoresheet (helper function)
    def test_create_base_score_sheet_redesign(self):
        scoresheet = create_base_score_sheet_redesign(division="senior")
        self.assertEqual(scoresheet.sheetType, ScoresheetEnum.REDESIGN)
        self.assertEqual(scoresheet.field1, 0.0)  # Innovation & Creativity
        self.assertEqual(scoresheet.field8, "senior")  # Division
        self.assertEqual(scoresheet.field9, "")  # Comments

    # Test retrieving scoresheet details by team
    def test_get_scoresheet_details_by_team_redesign(self):
        # Update scoresheet with some values
        self.scoresheet.field1 = 5.0  # Innovation & Creativity
        self.scoresheet.field2 = 4.0  # Use of Item
        self.scoresheet.save()

        url = reverse('get_scoresheet_details_by_team', args=[self.team.id])  # Adjust URL name if different
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        redesign_data = response.data["6"]  # Key "6" is for REDESIGN
        self.assertEqual(redesign_data["innovation_creativity"], [5.0])
        self.assertEqual(redesign_data["use_of_item"], [4.0])
        self.assertEqual(redesign_data["division"], ["junior"])

    # Test retrieving scoresheet details for a contest
    def test_get_scoresheet_details_for_contest(self):
        # Update scoresheet with some values
        self.scoresheet.field1 = 6.0  # Innovation & Creativity
        self.scoresheet.field2 = 5.0  # Use of Item
        self.scoresheet.save()

        url = reverse('get_scoresheet_details_for_contest')  # Adjust URL name if different
        data = {"contestid": self.contest.id}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        team_data = response.data["teams"][str(self.team.id)]
        redesign_data = team_data["6"]  # Key "6" is for REDESIGN
        self.assertEqual(redesign_data["innovation_creativity"], [6.0])
        self.assertEqual(redesign_data["use_of_item"], [5.0])
        self.assertEqual(redesign_data["division"], ["junior"])

    # Test creating scoresheets for teams in a cluster
    def test_create_sheets_for_teams_in_cluster(self):
        from ..views.scoresheets_redesign import create_sheets_for_teams_in_cluster
        created_sheets = create_sheets_for_teams_in_cluster(
            judge_id=self.judge.id,
            cluster_id=1,
            presentation=False,
            journal=False,
            mdo=False,
            runpenalties=False,
            otherpenalties=False,
            redesign=True,
            division="senior"
        )
        self.assertEqual(len(created_sheets), 1)  # One team in the cluster
        self.assertEqual(created_sheets[0]["sheetType"], ScoresheetEnum.REDESIGN)
        self.assertEqual(created_sheets[0]["division"], "senior")

    # Test deleting scoresheets for teams in a cluster
    def test_delete_sheets_for_teams_in_cluster(self):
        from ..views.scoresheets_redesign import delete_sheets_for_teams_in_cluster
        delete_sheets_for_teams_in_cluster(
            judge_id=self.judge.id,
            cluster_id=1,
            presentation=False,
            journal=False,
            mdo=False,
            runpenalties=False,
            otherpenalties=False,
            redesign=True
        )
        self.assertEqual(Scoresheet.objects.count(), 0)
        self.assertEqual(MapScoresheetToTeamJudge.objects.count(), 0)

    # Test edge case: invalid data for update_scores
    def test_update_scores_redesign_invalid_data(self):
        url = reverse('update_scores')
        data = {
            "id": self.scoresheet.id,
            "sheetType": ScoresheetEnum.REDESIGN,
            "innovation_creativity": "invalid",  # Invalid score (not a float)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test edge case: non-existent scoresheet
    def test_update_scores_non_existent(self):
        url = reverse('update_scores')
        data = {
            "id": 9999,  # Non-existent ID
            "sheetType": ScoresheetEnum.REDESIGN,
            "innovation_creativity": 5.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test edge case: unauthenticated request
    def test_update_scores_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('update_scores')
        data = {
            "id": self.scoresheet.id,
            "sheetType": ScoresheetEnum.REDESIGN,
            "innovation_creativity": 5.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)