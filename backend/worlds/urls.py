from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("worlds", views.WorldViewSet, basename="world")
router.register("characters", views.CharacterViewSet, basename="character")
router.register("relationships", views.RelationshipViewSet, basename="relationship")
router.register("skills", views.SkillViewSet, basename="skill")

urlpatterns = [
    path("", include(router.urls)),
]
