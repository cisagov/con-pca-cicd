from rest_framework import serializers


class TaskListSerializer(serializers.Serializer):
    active = serializers.DictField(child=serializers.CharField())
    scheduled = serializers.DictField(child=serializers.CharField())
    reserved = serializers.DictField(child=serializers.CharField())
    registered = serializers.DictField(child=serializers.CharField())


class CampaignReportSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    campaign_id = serializers.EmailField()
    time = serializers.DateTimeField()
    message = serializers.CharField()
    details = serializers.CharField()
