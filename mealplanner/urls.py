"""mealplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin

from core import views as core_views
from usersettings import views as usersettings_views
from planning import views as planning_views
from recipes import views as recipes_views

from rest_framework_jwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', core_views.UserViewSet)
router.register(r'profiles', usersettings_views.ProfileViewSet)
router.register(r'dris', usersettings_views.DRIViewSet)
router.register(r'dayplannings', planning_views.DayPlanningViewSet)
router.register(r'weekplannings', planning_views.WeekPlanningViewSet)
router.register(r'mealsettings', planning_views.MealSettingViewSet)
router.register(r'meals', planning_views.MealViewSet)
router.register(r'recipes', recipes_views.RecipeViewSet)
router.register(r'ingredients', recipes_views.IngredientTagViewSet)
router.register(r'groceries', recipes_views.IngredientViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', jwt_views.obtain_jwt_token),
]
