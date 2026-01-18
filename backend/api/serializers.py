from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.gis.geos import Point as PointObject

from geomessages.models import Point, Message


User = get_user_model()


class PasswordField(serializers.CharField):

    def to_internal_value(self, data):
        validate_password(data)
        return make_password(data)


class RegisterUserSerializer(serializers.ModelSerializer):
    password = PasswordField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


class PointSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    class Meta:
        model = Point
        fields = (
            'id',
            'longitude',
            'latitude'
        )
    
    def create(self, validated_data):
        longitude = validated_data.pop('longitude')
        latitude = validated_data.pop('latitude')
        validated_data['point'] = PointObject(longitude, latitude)
        return super().create(validated_data)
    
    def to_representation(self, instance):
        return_dict = dict()
        return_dict['id'] = instance.id
        return_dict['longitude'] = instance.point[0]
        return_dict['latitude'] = instance.point[1]
        return return_dict


class MessageSerializer(serializers.ModelSerializer):
    point_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Point.objects.all(),
        source='point'
    )
    point = PointSerializer(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Message
        fields = (
            'id',
            'author',
            'text',
            'point_id',
            'point'
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)