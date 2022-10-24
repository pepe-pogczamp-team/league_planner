from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from league_planner.views.league import LeagueViewSet
from league_planner.views.user import CreateUserView


router = SimpleRouter()
router.register("leagues", LeagueViewSet, "leagues")


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token),
    path('register/', CreateUserView.as_view()),
]
