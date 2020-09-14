from .models import Logs
from rest_framework.serializers import ModelSerializer


class LogsSerializer(ModelSerializer):
    class Meta:
        model = Logs
        fields = ('id', 'ip', 'created_at', 'user_id', 'description',
                  'button_id', 'component_id', 'event_id', 'agent', 'fired_at')
        read_only_fields = ('created_at',)
