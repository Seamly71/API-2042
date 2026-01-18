from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView

from api.views import RegisterViewSet, PointViewSet, MessageViewSet


auth_urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', TokenCreateView.as_view(), name='login'),
    path('logout/', TokenDestroyView.as_view(), name='logout'),
]

points_urlpatterns = [
    path('messages/search/', MessageViewSet.as_view({'get': 'list'}), name='find_messages'),
    path('messages/', MessageViewSet.as_view({'post': 'create'}), name='create_message'),
    path('search/', PointViewSet.as_view({'get': 'list'}), name='find_points'),
    path('', PointViewSet.as_view({'post': 'create'}), name='create_point'),
]


urlpatterns = (
    path('auth/', include(auth_urlpatterns)),
    path('points/', include(points_urlpatterns)),
)

app_name = 'api'