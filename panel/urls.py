from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
app_name = 'account'

urlpatterns = [
    path('sms/', Sms.as_view(), name='sms'),
    path('statistics/', Statistics.as_view(), name='statistics'),
    path('today-projects/', TodayProjectListAPI.as_view(), name='project-list'),
    path('not-tracked/', NotTrackedProjectListAPI.as_view(), name='project-list'),
    path('project-create/', ProjectCreateAPI.as_view(), name='project-create'),
    path('project/<int:projectId>/', ProjectRetrieveAPI.as_view(), name='project-retrieve'),
    path('project-update/', ProjectUpdateAPI.as_view(), name='project-update'),
    path('search/', ProjectSearch.as_view(), name='search_project'),

    path('authentication/', Authentication.as_view(), name="login-authenticaion"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('get-user/', GetUser.as_view(), name="get-user")

]
