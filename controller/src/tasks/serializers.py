from rest_framework import serializers


class CampaignReportSerializer(serializers.Serializer):
    task_id = serializers.CharField()
