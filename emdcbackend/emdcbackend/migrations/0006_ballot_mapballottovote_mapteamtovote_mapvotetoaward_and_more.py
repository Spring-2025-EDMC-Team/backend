# Generated by Django 5.0.2 on 2025-02-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emdcbackend', '0005_remove_specialaward_team_specialaward_teamid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestid', models.IntegerField()),
                ('isSubmitted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MapBallotToVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ballotid', models.IntegerField()),
                ('voteid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MapTeamToVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamid', models.IntegerField()),
                ('voteid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MapVoteToAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awardid', models.IntegerField()),
                ('voteid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votedteamid', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='specialaward',
            name='isJudge',
            field=models.BooleanField(default=False),
        ),
    ]
