from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventTypeMasterViewSet, CommitteeMasterViewSet, EventMasterViewSet

router = DefaultRouter()
router.register(r'master/event-types', EventTypeMasterViewSet, basename='event-types')
router.register(r'master/committees', CommitteeMasterViewSet, basename='committees')
router.register(r'master/events', EventMasterViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
]
