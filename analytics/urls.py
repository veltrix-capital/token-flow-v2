from django.urls import path
from .views import UserViewSet, BusinessViewSet, EventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = router.urls
