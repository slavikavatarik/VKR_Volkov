from rest_framework import serializers
from django.contrib.auth.models import User, Group
from courses.models import Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Пользователь с таким логином уже существует")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Добавляем в группу 'clients'
        group = Group.objects.get(name='clients')
        user.groups.add(group)

        # Создаем профиль клиента
        Client.objects.create(
            lname=' ',
            name=' ',
            phone=' ',
            img='images/clients/user.png',
            user=user
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'lname', 'name', 'phone', 'img', 'user']