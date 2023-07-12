from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_ecommerce_01.users.api.views import UserViewSet
from django_ecommerce_01.todos.views import TodoViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
# router.register("todos", TodoViewSet, basename='todos')



app_name = "api"
urlpatterns = router.urls
