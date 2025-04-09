# Generated by Django 5.0.2 on 2025-04-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emdcbackend', '0006_ballot_mapballottovote_mapteamtovote_mapvotetoaward_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapAwardToContest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestid', models.IntegerField()),
                ('awardid', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='judge',
            name='redesign',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teams',
            name='redesign_score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mapscoresheettoteamjudge',
            name='sheetType',
            field=models.IntegerField(choices=[(1, 'Presentation'), (2, 'Journal'), (3, 'Machinedesign'), (4, 'Runpenalties'), (5, 'Otherpenalties'), (6, 'Redesign')]),
        ),
        migrations.AlterField(
            model_name='scoresheet',
            name='sheetType',
            field=models.IntegerField(choices=[(1, 'Presentation'), (2, 'Journal'), (3, 'Machinedesign'), (4, 'Runpenalties'), (5, 'Otherpenalties'), (6, 'Redesign')]),
        ),
    ]
