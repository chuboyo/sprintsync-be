from rest_framework import routers
from users.views import UserViewset
from tasks.views import TaskViewSet

router = routers.DefaultRouter()
router.register("users", UserViewset, basename="user")
router.register("tasks", TaskViewSet, basename="task")