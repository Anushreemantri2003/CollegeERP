from rest_framework import serializers
from .models import EVENT_TYPE_MASTER, EVENT_MASTER, COMMITTEE_MASTER
from django.utils import timezone

class EventTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVENT_TYPE_MASTER
        fields = '__all__'

class CommitteeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = COMMITTEE_MASTER
        fields = '__all__'

class EventMasterSerializer(serializers.ModelSerializer):
    # EVENT_TYPE = EventTypeMasterSerializer(read_only=True)
    # ORGANIZED_BY = CommitteeMasterSerializer(read_only=True)
    # EVENT_TYPE_ID = serializers.PrimaryKeyRelatedField(
    #     queryset=EVENT_TYPE_MASTER.objects.all(), source='EVENT_TYPE', write_only=True
    # )
    # ORGANIZED_BY_ID = serializers.PrimaryKeyRelatedField(
    #     queryset=COMMITTEE_MASTER.objects.all(), source='ORGANIZED_BY', write_only=True
    # )

    class Meta:
        model = EVENT_MASTER
        fields = [
            'RECORD_ID', 'EVENT_TYPE', 
            'EVENT_NAME', 'ORGANIZED_BY',
            'EVENT_START_DT', 'EVENT_END_DT',
            'EVENT_PURPOSE', 'EVENT_REMARKS'
        ]

