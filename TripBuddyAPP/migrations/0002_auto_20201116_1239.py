# Generated by Django 3.1.3 on 2020-11-16 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TripBuddyAPP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='joiner',
            field=models.ManyToManyField(related_name='jointrips', to='TripBuddyAPP.User'),
        ),
    ]
