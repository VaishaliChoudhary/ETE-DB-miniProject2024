# Generated by Django 3.2.16 on 2024-07-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20240707_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='grade',
            field=models.CharField(choices=[('O', 'O'), ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'), ('C+', 'C+'), ('C', 'C'), ('F', 'F'), ('P', 'P'), ('NE', 'NE'), ('X', 'X'), ('I', 'I')], max_length=255),
        ),
    ]
