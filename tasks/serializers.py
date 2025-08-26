from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'total_minutes', 'created_at']
        read_only_fields = ['total_minutes', 'created_at', 'user']

    def update(self, instance, validated_data):
        # Detect status change
        new_status = validated_data.get('status', instance.status)
        prev_status = instance.status
        response = super().update(instance, validated_data)

        # If status changed to 'done', calculate duration
        if new_status == 'done' and prev_status != 'done':
            instance.calculate_duration()

        return response

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
