from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .Maps.MapScoreSheet import delete_score_sheet_mapping
from ..models import Scoresheet, Teams, Judge, MapClusterToTeam, MapScoresheetToTeamJudge, MapJudgeToCluster, ScoresheetEnum, Contest, MapContestToTeam
from ..serializers import ScoresheetSerializer, MapScoreSheetToTeamJudgeSerializer

@api_view(["GET"])
def scores_by_id(request, scores_id):
    scores = get_object_or_404(Scoresheet, id=scores_id)
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"ScoreSheet": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_score_sheet(request):
    map_data = request.data
    result = create_score_sheet_helper(map_data)
    if "errors" in result:
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_score_sheet(request):
    scores = get_object_or_404(Scoresheet, id=request.data["id"])
    scores.sheetType = request.data["sheetType"]
    scores.isSubmitted = request.data["isSubmitted"]
    
    if scores.sheetType == ScoresheetEnum.REDESIGN:
        scores.field1 = request.data.get("innovation_creativity", 0.0)
        scores.field2 = request.data.get("use_of_item", 0.0)
        scores.field3 = request.data.get("explanation_solution", 0.0)
        scores.field4 = request.data.get("engineering_principles", 0.0)
        scores.field5 = request.data.get("learning_identification", 0.0)
        scores.field6 = request.data.get("teamwork", 0.0)
        scores.field7 = request.data.get("communication", 0.0)
        scores.field8 = request.data.get("division", "junior")  # Default to junior
        scores.field9 = request.data.get("comments", "")
    elif scores.sheetType == ScoresheetEnum.OTHERPENALTIES:
        scores.field1 = request.data["field1"]
        scores.field2 = request.data["field2"]
        scores.field3 = request.data["field3"]
        scores.field4 = request.data["field4"]
        scores.field5 = request.data["field5"]
        scores.field6 = request.data["field6"]
        scores.field7 = request.data["field7"]
    else:
        scores.field1 = request.data["field1"]
        scores.field2 = request.data["field2"]
        scores.field3 = request.data["field3"]
        scores.field4 = request.data["field4"]
        scores.field5 = request.data["field5"]
        scores.field6 = request.data["field6"]
        scores.field7 = request.data["field7"]
        scores.field8 = request.data["field8"]
        scores.field9 = request.data["field9"]
        if scores.sheetType == ScoresheetEnum.RUNPENALTIES:
            scores.field10 = request.data["field10"]
            scores.field11 = request.data["field11"]
            scores.field12 = request.data["field12"]
            scores.field13 = request.data["field13"]
            scores.field14 = request.data["field14"]
            scores.field15 = request.data["field15"]
            scores.field16 = request.data["field16"]
            scores.field17 = request.data["field17"]
    
    scores.save()
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"edit_score_sheets": serializer.data})

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_scores(request):
    scores = get_object_or_404(Scoresheet, id=request.data["id"])
    
    if scores.sheetType == ScoresheetEnum.REDESIGN:
        scores.field1 = request.data.get("innovation_creativity", scores.field1)
        scores.field2 = request.data.get("use_of_item", scores.field2)
        scores.field3 = request.data.get("explanation_solution", scores.field3)
        scores.field4 = request.data.get("engineering_principles", scores.field4)
        scores.field5 = request.data.get("learning_identification", scores.field5)
        scores.field6 = request.data.get("teamwork", scores.field6)
        scores.field7 = request.data.get("communication", scores.field7)
        scores.field8 = request.data.get("division", scores.field8)
        scores.field9 = request.data.get("comments", scores.field9)
    elif scores.sheetType == ScoresheetEnum.OTHERPENALTIES:
        scores.field1 = request.data["field1"]
        scores.field2 = request.data["field2"]
        scores.field3 = request.data["field3"]
        scores.field4 = request.data["field4"]
        scores.field5 = request.data["field5"]
        scores.field6 = request.data["field6"]
        scores.field7 = request.data["field7"]
    else:
        scores.field1 = request.data["field1"]
        scores.field2 = request.data["field2"]
        scores.field3 = request.data["field3"]
        scores.field4 = request.data["field4"]
        scores.field5 = request.data["field5"]
        scores.field6 = request.data["field6"]
        scores.field7 = request.data["field7"]
        scores.field8 = request.data["field8"]
        scores.field9 = request.data["field9"]
        if scores.sheetType == ScoresheetEnum.RUNPENALTIES:
            scores.field10 = request.data["field10"]
            scores.field11 = request.data["field11"]
            scores.field12 = request.data["field12"]
            scores.field13 = request.data["field13"]
            scores.field14 = request.data["field14"]
            scores.field15 = request.data["field15"]
            scores.field16 = request.data["field16"]
            scores.field17 = request.data["field17"]
    
    scores.save()
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"updated_sheet": serializer.data})

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_score_sheet_field(request):
    sheet = get_object_or_404(Scoresheet, id=request.data["id"])
    
    field_name = ""
    if isinstance(request.data["field"], int):
        field_name = "field" + str(request.data["field"])
    else:
        field_name = request.data["field"]
    
    if hasattr(sheet, field_name):
        setattr(sheet, field_name, request.data["new_value"])
        sheet.save()
        serializer = ScoresheetSerializer(instance=sheet)
        return Response({"score_sheet": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid field"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_score_sheet(request, scores_id):
    scores = get_object_or_404(Scoresheet, id=scores_id)
    scores.delete()
    return Response({"detail": "Score Sheet deleted successfully."}, status=status.HTTP_200_OK)

def create_score_sheet_helper(map_data):
    serializer = ScoresheetSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return {"errors": serializer.errors}

def create_base_score_sheet(sheet_type):
    base_score_data = {
        "sheetType": sheet_type,
        "isSubmitted": False,
        "field1": 0.0,
        "field2": 0.0,
        "field3": 0.0,
        "field4": 0.0,
        "field5": 0.0,
        "field6": 0.0,
        "field7": 0.0,
        "field8": 0.0,
        "field9": "",
    }
    serializer = ScoresheetSerializer(data=base_score_data)
    if serializer.is_valid():
        score_sheet = serializer.save()
        return score_sheet
    else:
        raise ValidationError(serializer.errors)

def create_base_score_sheet_runpenalties():
    base_score_data = {
        "sheetType": ScoresheetEnum.RUNPENALTIES,
        "isSubmitted": False,
        "field1": 0.0,
        "field2": 0.0,
        "field3": 0.0,
        "field4": 0.0,
        "field5": 0.0,
        "field6": 0.0,
        "field7": 0.0,
        "field8": 0.0,
        "field9": "",
        "field10": 0.0,
        "field11": 0.0,
        "field12": 0.0,
        "field13": 0.0,
        "field14": 0.0,
        "field15": 0.0,
        "field16": 0.0,
        "field17": 0.0
    }
    serializer = ScoresheetSerializer(data=base_score_data)
    if serializer.is_valid():
        score_sheet = serializer.save()
        return score_sheet
    else:
        raise ValidationError(serializer.errors)

def create_base_score_sheet_otherpenalties():
    base_score_data = {
        "sheetType": ScoresheetEnum.OTHERPENALTIES,
        "isSubmitted": False,
        "field1": 0.0,
        "field2": 0.0,
        "field3": 0.0,
        "field4": 0.0,
        "field5": 0.0,
        "field6": 0.0,
        "field7": 0.0,
        "field9": ""
    }
    serializer = ScoresheetSerializer(data=base_score_data)
    if serializer.is_valid():
        score_sheet = serializer.save()
        return score_sheet
    else:
        raise ValidationError(serializer.errors)

def create_base_score_sheet_redesign(division="junior"):
    base_score_data = {
        "sheetType": ScoresheetEnum.REDESIGN,
        "isSubmitted": False,
        "field1": 0.0,  # Innovation & Creativity
        "field2": 0.0,  # Use of Item in Solution
        "field3": 0.0,  # Explanation of Solution
        "field4": 0.0,  # Explanation of Engineering & Science Principles
        "field5": 0.0,  # Identification of Learning
        "field6": 0.0,  # Teamwork
        "field7": 0.0,  # Communication
        "field8": division,  # Division (junior/senior)
        "field9": ""  # Comments/notes
    }
    serializer = ScoresheetSerializer(data=base_score_data)
    if serializer.is_valid():
        score_sheet = serializer.save()
        return score_sheet
    else:
        raise ValidationError(serializer.errors)

def create_sheets_for_teams_in_cluster(judge_id, cluster_id, presentation, journal, mdo, runpenalties, otherpenalties, redesign=False, division="junior"):
    try:
        mappings = MapClusterToTeam.objects.filter(clusterid=cluster_id)
        if not mappings.exists():
            raise ValidationError("No teams found for the specified cluster.")
        
        team_ids = mappings.values_list('teamid', flat=True)
        teams_in_cluster = Teams.objects.filter(id__in=team_ids)
        created_score_sheets = []
        
        for team in teams_in_cluster:
            if presentation:
                sheet = create_base_score_sheet(ScoresheetEnum.PRESENTATION)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.PRESENTATION}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({"team_id": team.id, "judge_id": judge_id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.PRESENTATION})
                else:
                    raise ValidationError(map_serializer.errors)
            if journal:
                sheet = create_base_score_sheet(ScoresheetEnum.JOURNAL)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.JOURNAL}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({"team_id": team.id, "judge_id": judge_id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.JOURNAL})
                else:
                    raise ValidationError(map_serializer.errors)
            if mdo:
                sheet = create_base_score_sheet(ScoresheetEnum.MACHINEDESIGN)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.MACHINEDESIGN}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({"team_id": team.id, "judge_id": judge_id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.MACHINEDESIGN})
                else:
                    raise ValidationError(map_serializer.errors)
            if runpenalties:
                sheet = create_base_score_sheet_runpenalties()
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.RUNPENALTIES}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({"team_id": team.id, "judge_id": judge_id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.RUNPENALTIES})
                else:
                    raise ValidationError(map_serializer.errors)
            if otherpenalties:
                sheet = create_base_score_sheet_otherpenalties()
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.OTHERPENALTIES}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({"team_id": team.id, "judge_id": judge_id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.OTHERPENALTIES})
                else:
                    raise ValidationError(map_serializer.errors)
            if redesign:
                sheet = create_base_score_sheet_redesign(division)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.REDESIGN}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({"team_id": team.id, "judge_id": judge_id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.REDESIGN, "division": division})
                else:
                    raise ValidationError(map_serializer.errors)
        
        return created_score_sheets
    except Exception as e:
        raise ValidationError({"detail": str(e)})

def create_score_sheets_for_team(team, judges):
    created_score_sheets = []
    for judge in judges:
        if judge.presentation:
            score_sheet = create_base_score_sheet(ScoresheetEnum.PRESENTATION)
            MapScoresheetToTeamJudge.objects.create(teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.PRESENTATION)
            created_score_sheets.append(score_sheet)
        if judge.journal:
            score_sheet = create_base_score_sheet(ScoresheetEnum.JOURNAL)
            MapScoresheetToTeamJudge.objects.create(teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.JOURNAL)
            created_score_sheets.append(score_sheet)
        if judge.mdo:
            score_sheet = create_base_score_sheet(ScoresheetEnum.MACHINEDESIGN)
            MapScoresheetToTeamJudge.objects.create(teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.MACHINEDESIGN)
            created_score_sheets.append(score_sheet)
        if judge.runpenalties:
            score_sheet = create_base_score_sheet_runpenalties()
            MapScoresheetToTeamJudge.objects.create(teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.RUNPENALTIES)
            created_score_sheets.append(score_sheet)
        if judge.otherpenalties:
            score_sheet = create_base_score_sheet_otherpenalties()
            MapScoresheetToTeamJudge.objects.create(teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.OTHERPENALTIES)
            created_score_sheets.append(score_sheet)
        if hasattr(judge, 'redesign') and judge.redesign:  # Assuming Judge model has a redesign attribute
            score_sheet = create_base_score_sheet_redesign(division="junior")  # Default division, could be parameterized
            MapScoresheetToTeamJudge.objects.create(teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.REDESIGN)
            created_score_sheets.append(score_sheet)
    return created_score_sheets

def get_scoresheet_id(judge_id, team_id, scoresheet_type):
    try:
        mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team_id, sheetType=scoresheet_type)
        scoresheet = Scoresheet.objects.get(id=mapping.scoresheetid)
        return scoresheet.id
    except (MapScoresheetToTeamJudge.DoesNotExist, Scoresheet.DoesNotExist):
        raise ValidationError({"error": "No scoresheet found"})

def delete_sheets_for_teams_in_cluster(judge_id, cluster_id, presentation, journal, mdo, runpenalties, otherpenalties, redesign=False):
    try:
        mappings = MapClusterToTeam.objects.filter(clusterid=cluster_id)
        if not mappings.exists():
            raise ValidationError("No teams found for the specified cluster.")
        
        team_ids = mappings.values_list('teamid', flat=True)
        teams_in_cluster = Teams.objects.filter(id__in=team_ids)
        
        for team in teams_in_cluster:
            if presentation:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, ScoresheetEnum.PRESENTATION)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=ScoresheetEnum.PRESENTATION)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if journal:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, ScoresheetEnum.JOURNAL)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=ScoresheetEnum.JOURNAL)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if mdo:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, ScoresheetEnum.MACHINEDESIGN)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=ScoresheetEnum.MACHINEDESIGN)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if runpenalties:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, ScoresheetEnum.RUNPENALTIES)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=ScoresheetEnum.RUNPENALTIES)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if otherpenalties:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, ScoresheetEnum.OTHERPENALTIES)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=ScoresheetEnum.OTHERPENALTIES)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if redesign:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, ScoresheetEnum.REDESIGN)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=ScoresheetEnum.REDESIGN)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
    except Exception as e:
        raise ValidationError({"detail": str(e)})

def make_sheets_for_team(teamid, clusterid):
    created_score_sheets = []
    judges = MapJudgeToCluster.objects.filter(clusterid=clusterid)
    for judge_map in judges:
        judge = Judge.objects.get(id=judge_map.judgeid)
        if judge.presentation:
            sheet = create_base_score_sheet(ScoresheetEnum.PRESENTATION)
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.PRESENTATION}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({"team_id": teamid, "judge_id": judge.id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.PRESENTATION})
            else:
                raise ValidationError(map_serializer.errors)
        if judge.journal:
            sheet = create_base_score_sheet(ScoresheetEnum.JOURNAL)
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.JOURNAL}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({"team_id": teamid, "judge_id": judge.id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.JOURNAL})
            else:
                raise ValidationError(map_serializer.errors)
        if judge.mdo:
            sheet = create_base_score_sheet(ScoresheetEnum.MACHINEDESIGN)
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.MACHINEDESIGN}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({"team_id": teamid, "judge_id": judge.id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.MACHINEDESIGN})
            else:
                raise ValidationError(map_serializer.errors)
        if judge.runpenalties:
            sheet = create_base_score_sheet_runpenalties()
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.RUNPENALTIES}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({"team_id": teamid, "judge_id": judge.id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.RUNPENALTIES})
            else:
                raise ValidationError(map_serializer.errors)
        if judge.otherpenalties:
            sheet = create_base_score_sheet_otherpenalties()
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.OTHERPENALTIES}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({"team_id": teamid, "judge_id": judge.id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.OTHERPENALTIES})
            else:
                raise ValidationError(map_serializer.errors)
        if hasattr(judge, 'redesign') and judge.redesign:
            sheet = create_base_score_sheet_redesign(division="junior")  # Default division
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.id, "sheetType": ScoresheetEnum.REDESIGN}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({"team_id": teamid, "judge_id": judge.id, "scoresheet_id": sheet.id, "sheetType": ScoresheetEnum.REDESIGN, "division": "junior"})
            else:
                raise ValidationError(map_serializer.errors)
    return created_score_sheets

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_scoresheet_details_by_team(request, team_id):
    scoresheet_mappings = MapScoresheetToTeamJudge.objects.filter(teamid=team_id)
    scoresheets = Scoresheet.objects.filter(id__in=scoresheet_mappings.values_list('scoresheetid', flat=True))
    
    presentation_scoresheet_details = [[] for _ in range(9)]
    journal_scoresheet_details = [[] for _ in range(9)]
    machinedesign_scoresheet_details = [[] for _ in range(9)]
    run_penalties_scoresheet_details = [[] for _ in range(16)]
    other_penalties_scoresheet_details = [[] for _ in range(7)]
    redesign_scoresheet_details = [[] for _ in range(9)]
    
    for sheet in scoresheets:
        if sheet.sheetType == ScoresheetEnum.PRESENTATION:
            presentation_scoresheet_details[0].append(sheet.field1)
            presentation_scoresheet_details[1].append(sheet.field2)
            presentation_scoresheet_details[2].append(sheet.field3)
            presentation_scoresheet_details[3].append(sheet.field4)
            presentation_scoresheet_details[4].append(sheet.field5)
            presentation_scoresheet_details[5].append(sheet.field6)
            presentation_scoresheet_details[6].append(sheet.field7)
            presentation_scoresheet_details[7].append(sheet.field8)
            presentation_scoresheet_details[8].append(sheet.field9)
        elif sheet.sheetType == ScoresheetEnum.JOURNAL:
            journal_scoresheet_details[0].append(sheet.field1)
            journal_scoresheet_details[1].append(sheet.field2)
            journal_scoresheet_details[2].append(sheet.field3)
            journal_scoresheet_details[3].append(sheet.field4)
            journal_scoresheet_details[4].append(sheet.field5)
            journal_scoresheet_details[5].append(sheet.field6)
            journal_scoresheet_details[6].append(sheet.field7)
            journal_scoresheet_details[7].append(sheet.field8)
            journal_scoresheet_details[8].append(sheet.field9)
        elif sheet.sheetType == ScoresheetEnum.MACHINEDESIGN:
            machinedesign_scoresheet_details[0].append(sheet.field1)
            machinedesign_scoresheet_details[1].append(sheet.field2)
            machinedesign_scoresheet_details[2].append(sheet.field3)
            machinedesign_scoresheet_details[3].append(sheet.field4)
            machinedesign_scoresheet_details[4].append(sheet.field5)
            machinedesign_scoresheet_details[5].append(sheet.field6)
            machinedesign_scoresheet_details[6].append(sheet.field7)
            machinedesign_scoresheet_details[7].append(sheet.field8)
            machinedesign_scoresheet_details[8].append(sheet.field9)
        elif sheet.sheetType == ScoresheetEnum.RUNPENALTIES:
            run_penalties_scoresheet_details[0].append(sheet.field1)
            run_penalties_scoresheet_details[1].append(sheet.field2)
            run_penalties_scoresheet_details[2].append(sheet.field3)
            run_penalties_scoresheet_details[3].append(sheet.field4)
            run_penalties_scoresheet_details[4].append(sheet.field5)
            run_penalties_scoresheet_details[5].append(sheet.field6)
            run_penalties_scoresheet_details[6].append(sheet.field7)
            run_penalties_scoresheet_details[7].append(sheet.field8)
            run_penalties_scoresheet_details[8].append(sheet.field10)
            run_penalties_scoresheet_details[9].append(sheet.field11)
            run_penalties_scoresheet_details[10].append(sheet.field12)
            run_penalties_scoresheet_details[11].append(sheet.field13)
            run_penalties_scoresheet_details[12].append(sheet.field14)
            run_penalties_scoresheet_details[13].append(sheet.field15)
            run_penalties_scoresheet_details[14].append(sheet.field16)
            run_penalties_scoresheet_details[15].append(sheet.field17)
        elif sheet.sheetType == ScoresheetEnum.OTHERPENALTIES:
            other_penalties_scoresheet_details[0].append(sheet.field1)
            other_penalties_scoresheet_details[1].append(sheet.field2)
            other_penalties_scoresheet_details[2].append(sheet.field3)
            other_penalties_scoresheet_details[3].append(sheet.field4)
            other_penalties_scoresheet_details[4].append(sheet.field5)
            other_penalties_scoresheet_details[5].append(sheet.field6)
            other_penalties_scoresheet_details[6].append(sheet.field7)
        elif sheet.sheetType == ScoresheetEnum.REDESIGN:
            redesign_scoresheet_details[0].append(sheet.field1)  # Innovation & Creativity
            redesign_scoresheet_details[1].append(sheet.field2)  # Use of Item
            redesign_scoresheet_details[2].append(sheet.field3)  # Explanation of Solution
            redesign_scoresheet_details[3].append(sheet.field4)  # Engineering Principles
            redesign_scoresheet_details[4].append(sheet.field5)  # Learning Identification
            redesign_scoresheet_details[5].append(sheet.field6)  # Teamwork
            redesign_scoresheet_details[6].append(sheet.field7)  # Communication
            redesign_scoresheet_details[7].append(sheet.field8)  # Division
            redesign_scoresheet_details[8].append(sheet.field9)  # Comments
    
    presentation_scoresheet_response = {
        "1": presentation_scoresheet_details[0],
        "2": presentation_scoresheet_details[1],
        "3": presentation_scoresheet_details[2],
        "4": presentation_scoresheet_details[3],
        "5": presentation_scoresheet_details[4],
        "6": presentation_scoresheet_details[5],
        "7": presentation_scoresheet_details[6],
        "8": presentation_scoresheet_details[7],
        "9": presentation_scoresheet_details[8],
    }
    journal_scoresheet_response = {
        "1": journal_scoresheet_details[0],
        "2": journal_scoresheet_details[1],
        "3": journal_scoresheet_details[2],
        "4": journal_scoresheet_details[3],
        "5": journal_scoresheet_details[4],
        "6": journal_scoresheet_details[5],
        "7": journal_scoresheet_details[6],
        "8": journal_scoresheet_details[7],
        "9": journal_scoresheet_details[8],
    }
    machinedesign_scoresheet_response = {
        "1": machinedesign_scoresheet_details[0],
        "2": machinedesign_scoresheet_details[1],
        "3": machinedesign_scoresheet_details[2],
        "4": machinedesign_scoresheet_details[3],
        "5": machinedesign_scoresheet_details[4],
        "6": machinedesign_scoresheet_details[5],
        "7": machinedesign_scoresheet_details[6],
        "8": machinedesign_scoresheet_details[7],
        "9": machinedesign_scoresheet_details[8],
    }
    runpenalties_scoresheet_response = {
        "1": run_penalties_scoresheet_details[0],
        "2": run_penalties_scoresheet_details[1],
        "3": run_penalties_scoresheet_details[2],
        "4": run_penalties_scoresheet_details[3],
        "5": run_penalties_scoresheet_details[4],
        "6": run_penalties_scoresheet_details[5],
        "7": run_penalties_scoresheet_details[6],
        "8": run_penalties_scoresheet_details[7],
        "10": run_penalties_scoresheet_details[8],
        "11": run_penalties_scoresheet_details[9],
        "12": run_penalties_scoresheet_details[10],
        "13": run_penalties_scoresheet_details[11],
        "14": run_penalties_scoresheet_details[12],
        "15": run_penalties_scoresheet_details[13],
        "16": run_penalties_scoresheet_details[14],
        "17": run_penalties_scoresheet_details[15],
    }
    otherpenalties_scoresheet_response = {
        "1": other_penalties_scoresheet_details[0],
        "2": other_penalties_scoresheet_details[1],
        "3": other_penalties_scoresheet_details[2],
        "4": other_penalties_scoresheet_details[3],
        "5": other_penalties_scoresheet_details[4],
        "6": other_penalties_scoresheet_details[5],
        "7": other_penalties_scoresheet_details[6],
    }
    redesign_scoresheet_response = {
        "innovation_creativity": redesign_scoresheet_details[0],
        "use_of_item": redesign_scoresheet_details[1],
        "explanation_solution": redesign_scoresheet_details[2],
        "engineering_principles": redesign_scoresheet_details[3],
        "learning_identification": redesign_scoresheet_details[4],
        "teamwork": redesign_scoresheet_details[5],
        "communication": redesign_scoresheet_details[6],
        "division": redesign_scoresheet_details[7],
        "comments": redesign_scoresheet_details[8],
    }
    
    return Response({
        "1": presentation_scoresheet_response,
        "2": journal_scoresheet_response,
        "3": machinedesign_scoresheet_response,
        "4": runpenalties_scoresheet_response,
        "5": otherpenalties_scoresheet_response,
        "6": redesign_scoresheet_response
    }, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_scoresheet_details_for_contest(request):
    contest = get_object_or_404(Contest, id=request.data["contestid"])
    team_mappings = MapContestToTeam.objects.filter(contestid=contest.id)
    team_responses = {}
    
    for mapping in team_mappings:
        team = get_object_or_404(Teams, id=mapping.teamid)
        scoresheet_mappings = MapScoresheetToTeamJudge.objects.filter(teamid=team.id)
        scoresheets = Scoresheet.objects.filter(id__in=scoresheet_mappings.values_list('scoresheetid', flat=True))
        
        presentation_scoresheet_details = [[] for _ in range(9)]
        journal_scoresheet_details = [[] for _ in range(9)]
        machinedesign_scoresheet_details = [[] for _ in range(9)]
        run_penalties_scoresheet_details = [[] for _ in range(16)]
        other_penalties_scoresheet_details = [[] for _ in range(7)]
        redesign_scoresheet_details = [[] for _ in range(9)]
        
        for sheet in scoresheets:
            if sheet.sheetType == ScoresheetEnum.PRESENTATION:
                presentation_scoresheet_details[0].append(sheet.field1)
                presentation_scoresheet_details[1].append(sheet.field2)
                presentation_scoresheet_details[2].append(sheet.field3)
                presentation_scoresheet_details[3].append(sheet.field4)
                presentation_scoresheet_details[4].append(sheet.field5)
                presentation_scoresheet_details[5].append(sheet.field6)
                presentation_scoresheet_details[6].append(sheet.field7)
                presentation_scoresheet_details[7].append(sheet.field8)
                presentation_scoresheet_details[8].append(sheet.field9)
            elif sheet.sheetType == ScoresheetEnum.JOURNAL:
                journal_scoresheet_details[0].append(sheet.field1)
                journal_scoresheet_details[1].append(sheet.field2)
                journal_scoresheet_details[2].append(sheet.field3)
                journal_scoresheet_details[3].append(sheet.field4)
                journal_scoresheet_details[4].append(sheet.field5)
                journal_scoresheet_details[5].append(sheet.field6)
                journal_scoresheet_details[6].append(sheet.field7)
                journal_scoresheet_details[7].append(sheet.field8)
                journal_scoresheet_details[8].append(sheet.field9)
            elif sheet.sheetType == ScoresheetEnum.MACHINEDESIGN:
                machinedesign_scoresheet_details[0].append(sheet.field1)
                machinedesign_scoresheet_details[1].append(sheet.field2)
                machinedesign_scoresheet_details[2].append(sheet.field3)
                machinedesign_scoresheet_details[3].append(sheet.field4)
                machinedesign_scoresheet_details[4].append(sheet.field5)
                machinedesign_scoresheet_details[5].append(sheet.field6)
                machinedesign_scoresheet_details[6].append(sheet.field7)
                machinedesign_scoresheet_details[7].append(sheet.field8)
                machinedesign_scoresheet_details[8].append(sheet.field9)
            elif sheet.sheetType == ScoresheetEnum.RUNPENALTIES:
                run_penalties_scoresheet_details[0].append(sheet.field1)
                run_penalties_scoresheet_details[1].append(sheet.field2)
                run_penalties_scoresheet_details[2].append(sheet.field3)
                run_penalties_scoresheet_details[3].append(sheet.field4)
                run_penalties_scoresheet_details[4].append(sheet.field5)
                run_penalties_scoresheet_details[5].append(sheet.field6)
                run_penalties_scoresheet_details[6].append(sheet.field7)
                run_penalties_scoresheet_details[7].append(sheet.field8)
                run_penalties_scoresheet_details[8].append(sheet.field10)
                run_penalties_scoresheet_details[9].append(sheet.field11)
                run_penalties_scoresheet_details[10].append(sheet.field12)
                run_penalties_scoresheet_details[11].append(sheet.field13)
                run_penalties_scoresheet_details[12].append(sheet.field14)
                run_penalties_scoresheet_details[13].append(sheet.field15)
                run_penalties_scoresheet_details[14].append(sheet.field16)
                run_penalties_scoresheet_details[15].append(sheet.field17)
            elif sheet.sheetType == ScoresheetEnum.OTHERPENALTIES:
                other_penalties_scoresheet_details[0].append(sheet.field1)
                other_penalties_scoresheet_details[1].append(sheet.field2)
                other_penalties_scoresheet_details[2].append(sheet.field3)
                other_penalties_scoresheet_details[3].append(sheet.field4)
                other_penalties_scoresheet_details[4].append(sheet.field5)
                other_penalties_scoresheet_details[5].append(sheet.field6)
                other_penalties_scoresheet_details[6].append(sheet.field7)
            elif sheet.sheetType == ScoresheetEnum.REDESIGN:
                redesign_scoresheet_details[0].append(sheet.field1)
                redesign_scoresheet_details[1].append(sheet.field2)
                redesign_scoresheet_details[2].append(sheet.field3)
                redesign_scoresheet_details[3].append(sheet.field4)
                redesign_scoresheet_details[4].append(sheet.field5)
                redesign_scoresheet_details[5].append(sheet.field6)
                redesign_scoresheet_details[6].append(sheet.field7)
                redesign_scoresheet_details[7].append(sheet.field8)
                redesign_scoresheet_details[8].append(sheet.field9)
        
        presentation_scoresheet_response = {
            "1": presentation_scoresheet_details[0],
            "2": presentation_scoresheet_details[1],
            "3": presentation_scoresheet_details[2],
            "4": presentation_scoresheet_details[3],
            "5": presentation_scoresheet_details[4],
            "6": presentation_scoresheet_details[5],
            "7": presentation_scoresheet_details[6],
            "8": presentation_scoresheet_details[7],
            "9": presentation_scoresheet_details[8],
        }
        journal_scoresheet_response = {
            "1": journal_scoresheet_details[0],
            "2": journal_scoresheet_details[1],
            "3": journal_scoresheet_details[2],
            "4": journal_scoresheet_details[3],
            "5": journal_scoresheet_details[4],
            "6": journal_scoresheet_details[5],
            "7": journal_scoresheet_details[6],
            "8": journal_scoresheet_details[7],
            "9": journal_scoresheet_details[8],
        }
        machinedesign_scoresheet_response = {
            "1": machinedesign_scoresheet_details[0],
            "2": machinedesign_scoresheet_details[1],
            "3": machinedesign_scoresheet_details[2],
            "4": machinedesign_scoresheet_details[3],
            "5": machinedesign_scoresheet_details[4],
            "6": machinedesign_scoresheet_details[5],
            "7": machinedesign_scoresheet_details[6],
            "8": machinedesign_scoresheet_details[7],
            "9": machinedesign_scoresheet_details[8],
        }
        runpenalties_scoresheet_response = {
            "1": run_penalties_scoresheet_details[0],
            "2": run_penalties_scoresheet_details[1],
            "3": run_penalties_scoresheet_details[2],
            "4": run_penalties_scoresheet_details[3],
            "5": run_penalties_scoresheet_details[4],
            "6": run_penalties_scoresheet_details[5],
            "7": run_penalties_scoresheet_details[6],
            "8": run_penalties_scoresheet_details[7],
            "10": run_penalties_scoresheet_details[8],
            "11": run_penalties_scoresheet_details[9],
            "12": run_penalties_scoresheet_details[10],
            "13": run_penalties_scoresheet_details[11],
            "14": run_penalties_scoresheet_details[12],
            "15": run_penalties_scoresheet_details[13],
            "16": run_penalties_scoresheet_details[14],
            "17": run_penalties_scoresheet_details[15],
        }
        otherpenalties_scoresheet_response = {
            "1": other_penalties_scoresheet_details[0],
            "2": other_penalties_scoresheet_details[1],
            "3": other_penalties_scoresheet_details[2],
            "4": other_penalties_scoresheet_details[3],
            "5": other_penalties_scoresheet_details[4],
            "6": other_penalties_scoresheet_details[5],
            "7": other_penalties_scoresheet_details[6],
        }
        redesign_scoresheet_response = {
            "innovation_creativity": redesign_scoresheet_details[0],
            "use_of_item": redesign_scoresheet_details[1],
            "explanation_solution": redesign_scoresheet_details[2],
            "engineering_principles": redesign_scoresheet_details[3],
            "learning_identification": redesign_scoresheet_details[4],
            "teamwork": redesign_scoresheet_details[5],
            "communication": redesign_scoresheet_details[6],
            "division": redesign_scoresheet_details[7],
            "comments": redesign_scoresheet_details[8],
        }
        
        team_responses[team.id] = {
            "team_id": team.id,
            "1": presentation_scoresheet_response,
            "2": journal_scoresheet_response,
            "3": machinedesign_scoresheet_response,
            "4": runpenalties_scoresheet_response,
            "5": otherpenalties_scoresheet_response,
            "6": redesign_scoresheet_response
        }
    
    return Response({"teams": team_responses}, status=status.HTTP_200_OK)