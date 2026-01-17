from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Point, Message
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """
    Пользователи
    """
    class Meta:
        model = User
        fields = ['id', 'username']
        
class MessageSerializer(serializers.ModelSerializer):
    """
    Сообщения
    """
    user = UserSerializer(read_only=True)
    point_id = serializers.IntegerField(write_only=True)
    
    
    class Meta:
        model = Message
        fields = ['id', 'point', 'point_id', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'point', 'created_at']



class MessagePointSerializer(serializers.ModelSerializer):
    """
    Сообщения при просмотре точек
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['user', 'text', 'created_at']
        read_only_fields = ['user', 'text', 'created_at']





class PointSerializer(serializers.ModelSerializer):
    """
    Точки
    """
    user = UserSerializer(read_only=True)
    messages = MessagePointSerializer(many=True, read_only=True)

    
    class Meta:
        model = Point
        fields = ['id', 'user', 'name', 'latitude', 'longitude', 'created_at', 'messages']
        read_only_fields = ['id', 'user', 'created_at']
    
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Широта должна быть в диапазоне от -90 до 90")
        return value
    
    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Долгота должна быть в диапазоне от -180 до 180")
        return value



class PointSearchSerializer(serializers.Serializer):
    """
    Поиск точек
    """
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    radius = serializers.FloatField(required=True, min_value=0.1, max_value=1000)
    
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Широта должна быть в диапазоне от -90 до 90")
        return value
    
    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Долгота должна быть в диапазоне от -180 до 180")
        return value
    


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Регистрация пользователей
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user