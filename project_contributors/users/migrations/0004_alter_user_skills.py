# Generated by Django 3.2.9 on 2021-11-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='skills',
            field=models.CharField(default='[]', max_length=255),
        ),
    ]
