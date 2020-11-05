# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class CentroidCount(models.Model):
    id_centroid_count = models.AutoField(primary_key=True)
    id_observation = models.ForeignKey('Observation', models.DO_NOTHING, db_column='id_observation', blank=True, null=True)
    step = models.SmallIntegerField(blank=True, null=True)
    centroid = models.SmallIntegerField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centroid_count'

    def __str__(self):
        return 'Oberservation ID: %s , Step: %s' % (self.id_observation, self.step)



class Observation(models.Model):
    id_observation = models.SmallAutoField(primary_key=True)
    observation = models.CharField(max_length=37, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'observation'

    def __str__(self):
        return str(self.id_observation)

class Ypixels(models.Model):
    id_ypixels = models.AutoField(primary_key=True)
    id_observation = models.ForeignKey(Observation, models.DO_NOTHING, db_column='id_observation', blank=True, null=True)
    step = models.SmallIntegerField(blank=True, null=True)
    ypixels = models.TextField(blank=True, null=True)  # This field type is a guess.
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ypixels'

    def __str__(self):
        return str(self.id_observation), str(self.step)

# TODO: define how to select observations base on arrays
class observation_selection(models.Model):
    pass