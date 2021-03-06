# Generated by Django 3.1.2 on 2020-12-28 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centroid_webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id_image', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(blank=True, max_length=75, null=True)),
                ('slit_pos', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'images',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='observation_selection',
        ),
        migrations.AlterModelOptions(
            name='centroidcount',
            options={'managed': False, 'ordering': ['id_observation', 'step', 'centroid']},
        ),
    ]
