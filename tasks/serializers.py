from rest_framework import serializers
from .models import Task
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
    
    
class TaskDescriptionDraftSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    
    def generate_description(self):
        """
        Generates a task description from a short title using OpenAI GPT.
        """
        title = self.validated_data['title']
        prompt = f"""
        You are an expert project assistant. 
        Your task is to take a short task title and expand it into a detailed, clear, 
        and professional description. 

        Title: "{title}"

        Provide a concise but informative description (2–3 sentences) that explains:
        1. What needs to be done
        2. Why it matters
        3. Any key steps or considerations (if applicable)

        Make it actionable and human-friendly.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful task description generator."},
                      {"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        print(response)

        return response.choices[0].message.content
