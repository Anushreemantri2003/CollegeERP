
import os
from django.db import models
from core.models import AuditModel
from django.utils import timezone




class EVENT_TYPE_MASTER(AuditModel):
    RECORD_ID = models.AutoField(primary_key=True, db_column='RECORD_ID')
    MAIN_TYPE = models.CharField(max_length=100, db_column='MAIN_TYPE')
    SUB_TYPE = models.CharField(max_length=100, db_column='SUB_TYPE')

    class Meta:
        db_table =  '"COMMITTEE"."EVENT_TYPE_MASTER"'
        verbose_name = 'Event Type Master'
        verbose_name_plural = 'Event Type Masters'

    def __str__(self):
        return f"{self.MAIN_TYPE} - {self.SUBTYPE}"


class EVENT_MASTER(AuditModel):
    RECORD_ID = models.AutoField(primary_key=True, db_column='RECORD_ID')
    EVENT_TYPE = models.ForeignKey('EVENT_TYPE_MASTER', on_delete=models.CASCADE, db_column='EVENT_TYPE')
    EVENT_NAME = models.CharField(max_length=200, db_column='EVENT_NAME')
    ORGANIZED_BY = models.ForeignKey('COMMITTEE_MASTER', on_delete=models.CASCADE, db_column='ORGANIZED_BY')
    EVENT_START_DT = models.DateField(db_column='EVENT_START_DT')
    EVENT_END_DT = models.DateField(db_column='EVENT_END_DT')
    EVENT_PURPOSE = models.TextField(null=True, blank=True,db_column='EVENT_PURPOSE')
    EVENT_REMARKS = models.TextField(null=True, blank=True, db_column='EVENT_REMARKS')

    class Meta:
        db_table = '"COMMITTEE"."EVENT_MASTER"'
        verbose_name = 'Event Master'
        verbose_name_plural = 'Event Masters'

    def __str__(self):
        return self.EVENT_NAME
    


class COMMITTEE_MASTER(AuditModel):
    RECORD_ID = models.AutoField(primary_key=True, db_column='RECORD_ID')
    COM_NAME = models.CharField(max_length=200, db_column='COM_NAME')
    COM_FORMATION_DATE = models.DateField(db_column='COM_FORMATION_DATE')
    ACTIVE = models.CharField(max_length=1, db_column='ACTIVE')
    LEVEL1 = models.CharField(max_length=100, db_column='LEVEL1')
    REMARKS = models.TextField(null=True, blank=True, db_column='REMARKS')

    class Meta:
        db_table ='"COMMITTEE"."COMMITTEE_MASTER"'
        verbose_name = 'Committee Master'
        verbose_name_plural = 'Committee Masters'

    def __str__(self):
        return self.COM_NAME







# Create your models here.
