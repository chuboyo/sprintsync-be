from rest_framework import routers
from users.views import UserViewset

router = routers.DefaultRouter()
router.register("users", UserViewset, basename="user")