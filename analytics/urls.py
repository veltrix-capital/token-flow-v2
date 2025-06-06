from django.urls import path
from .views import UserListView, BusinessListView, EventListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='api-users'),
    path('businesses/', BusinessListView.as_view(), name='api-businesses'),
    path('events/', EventListView.as_view(), name='api-events'),
]
