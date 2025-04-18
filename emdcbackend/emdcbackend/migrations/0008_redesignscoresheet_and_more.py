# Generated by Django 5.1.1 on 2025-04-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emdcbackend', '0007_mapawardtocontest_judge_redesign_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedesignScoresheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamid', models.IntegerField()),
                ('judgeid', models.IntegerField()),
                ('isSubmitted', models.BooleanField(default=False)),
                ('field1', models.FloatField(blank=True, null=True)),
                ('field2', models.FloatField(blank=True, null=True)),
                ('field3', models.FloatField(blank=True, null=True)),
                ('field4', models.FloatField(blank=True, null=True)),
                ('field5', models.FloatField(blank=True, null=True)),
                ('field6', models.FloatField(blank=True, null=True)),
                ('field7', models.FloatField(blank=True, null=True)),
                ('field8', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='mapscoresheettoteamjudge',
            name='sheetType',
            field=models.IntegerField(choices=[(1, 'Presentation'), (2, 'Journal'), (3, 'Machinedesign'), (4, 'Runpenalties'), (5, 'Otherpenalties')]),
        ),
        migrations.AlterField(
            model_name='scoresheet',
            name='sheetType',
            field=models.IntegerField(choices=[(1, 'Presentation'), (2, 'Journal'), (3, 'Machinedesign'), (4, 'Runpenalties'), (5, 'Otherpenalties')]),
        ),
    ]
