from rest_framework import serializers


class CampaignSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    created_date = serializers.DateTimeField()
    launch_date = serializers.DateTimeField()
    status = serializers.CharField(max_length=50)
