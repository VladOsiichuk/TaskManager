from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Class to represent users in json data"""
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": 'password'}, write_only=True)
    password2 = serializers.CharField(style={"input_type": 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        pw = data.get('password')
        pw2 = data.pop('password2')

        if pw != pw2:
            # gg
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        user = User(username=validated_data.get('username'),
                    email=validated_data.get('email'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'))
        user.set_password(validated_data.get('password'))
        user.save()

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]
