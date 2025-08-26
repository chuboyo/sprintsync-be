from rest_framework import viewsets, permissions, decorators, response, status
from django.utils import timezone
from django.db.models import Sum
from .models import Task
from .serializers import TaskSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    @decorators.action(detail=False, methods=['get'])
    def daily_summary(self, request):
        """
        Returns total tasks and total duration for today's tasks for the current user.
        """
        today = timezone.now().date()
        tasks_today = self.get_queryset().filter(created_at__date=today)
        total_tasks = tasks_today.count()
        total_duration = tasks_today.aggregate(duration=Sum('total_minutes'))['duration']

        return response.Response({
            'total_tasks': total_tasks,
            'total_duration': total_duration
        }, status=status.HTTP_200_OK)

