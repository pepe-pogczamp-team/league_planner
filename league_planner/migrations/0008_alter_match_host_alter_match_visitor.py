# Generated by Django 4.1.3 on 2022-12-02 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_planner', '0007_alter_team_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='host', to='league_planner.team', verbose_name='Host Team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='visitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitor', to='league_planner.team', verbose_name='Visitor Team'),
        ),
    ]
