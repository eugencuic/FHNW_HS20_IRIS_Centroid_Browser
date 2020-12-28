# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

class CentroidCount(models.Model):
    id_centroid_count = models.AutoField(primary_key=True)
    id_observation = models.ForeignKey('Observation', models.DO_NOTHING, db_column='id_observation', blank=True, null=True)
    step = models.SmallIntegerField(blank=True, null=True)
    centroid = models.SmallIntegerField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'centroid_count'
        ordering = ['id_observation', 'step', 'centroid']

    def __str__(self):
        return 'Observation: %s' % (self.id_observation)

class Images(models.Model):
    id_image = models.AutoField(primary_key=True)
    path = models.CharField(max_length=75, blank=True, null=True)
    slit_pos = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'

class Observation(models.Model):
    id_observation = models.SmallAutoField(primary_key=True)
    observation = models.CharField(max_length=26, blank=True, null=True)
    x_pixels = models.SmallIntegerField(blank=True, null=True)
    y_pixels = models.SmallIntegerField(blank=True, null=True)
    n_steps = models.SmallIntegerField(blank=True, null=True)
    hek_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'observation'
        ordering = ['id_observation']

    def __str__(self):
        return 'Observation ID: %s' %(self.observation)

class Ypixels(models.Model):
    id_ypixels = models.AutoField(primary_key=True)
    id_observation = models.ForeignKey(Observation, models.DO_NOTHING, db_column='id_observation', blank=True, null=True)
    step = models.SmallIntegerField(blank=True, null=True)
    ypixels = models.TextField(blank=True, null=True) 
    l_1330 = models.ForeignKey(Images, models.DO_NOTHING, db_column='L_1330', related_name='+', blank=True, null=True)  # Field name made lowercase.
    l_1400 = models.ForeignKey(Images, models.DO_NOTHING, db_column='L_1400', related_name='+', blank=True, null=True)  # Field name made lowercase.
    l_2796 = models.ForeignKey(Images, models.DO_NOTHING, db_column='L_2796', related_name='+', blank=True, null=True)  # Field name made lowercase.
    l_2832 = models.ForeignKey(Images, models.DO_NOTHING, db_column='L_2832', related_name='+', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ypixels'
        ordering =  ['id_observation', 'step']

    def __str__(self):
        return 'Centroid ID: %s, Step: %s, 1330: %s, 1400:%s, 2796: %s, 2832: %s' % (self.id_observation, 
                                                                                        self.step,
                                                                                        self.l_1330,
                                                                                        self.l_1400,
                                                                                        self.l_2796,
                                                                                        self.l_2832
                                                                                        )
