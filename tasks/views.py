from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum, Count
from .models import Task
from .serializers import TaskSerializer, TaskDescriptionDraftSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == "draft_description":
            return TaskDescriptionDraftSerializer
        return TaskSerializer

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        """
        Returns total tasks and total duration for today's tasks for the current user.
        """
        today = timezone.now().date()
        tasks_today =  (
            self.get_queryset()
            .filter(created_at__date=today)
            .values('user__id', 'user__username')  # Group by user
            .annotate(
                total_tasks=Count('id'),
                total_duration=Sum('total_minutes')
            )
        )

        return Response(tasks_today, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def draft_description(self, request):
        """
        Generate a draft description from a given title without saving a task.
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        description = serializer.generate_description()
        return Response({"description": description},
                        status=status.HTTP_200_OK)

