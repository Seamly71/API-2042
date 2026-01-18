from rest_framework import viewsets, mixins, permissions
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point as PointObject
from django.contrib.gis.measure import Distance

from api.serializers import RegisterUserSerializer, PointSerializer, MessageSerializer
from api.paginators import APIPagination
from geomessages.models import Point, Message

User = get_user_model()


class RegisterViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)


class PointViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = APIPagination

    def get_queryset(self):
        if self.action != 'list':
            return super().get_queryset()

        longitude_str = self.request.query_params.get('longitude')
        latitude_str = self.request.query_params.get('latitude')
        radius_str = self.request.query_params.get('radius')

        error_dict = dict()
        if longitude_str is None:
            error_dict['longitude'] = 'Обязательный параметр.'
        if latitude_str is None:
            error_dict['latitude'] = 'Обязательный параметр.'
        if radius_str is None:
            error_dict['radius'] = 'Обязательный параметр.'
        if len(error_dict) != 0:
            raise ValidationError(error_dict)

        center = PointObject(float(longitude_str), float(latitude_str))
        return Point.objects.filter(
            point__dwithin=(center, Distance(km=float(radius_str)))
        )


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Message.objects.select_related("point")
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = APIPagination

    def get_queryset(self):
        if self.action != 'list':
            return super().get_queryset()

        longitude_str = self.request.query_params.get('longitude')
        latitude_str = self.request.query_params.get('latitude')
        radius_str = self.request.query_params.get('radius')

        error_dict = dict()
        if longitude_str is None:
            error_dict['longitude'] = 'Обязательный параметр.'
        if latitude_str is None:
            error_dict['latitude'] = 'Обязательный параметр.'
        if radius_str is None:
            error_dict['radius'] = 'Обязательный параметр.'
        if len(error_dict) != 0:
            raise ValidationError(error_dict)

        center = PointObject(float(longitude_str), float(latitude_str))
        return Message.objects.select_related("point").filter(
            point__point__dwithin=(center, Distance(km=float(radius_str)))
        )