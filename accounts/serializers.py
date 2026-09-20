from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='student',
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['role'] = user.role

        return token


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'is_active',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'role',
            'is_active',
            'created_at',
        ]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    # def validate_old_password(self, value):
    #     user = self.context['request'].user

    #     if not user.check_password(value):
    #         raise serializers.ValidationError(
    #             'Old password is incorrect.'
    #         )

    #     return value

    # def validate(self, attrs):
    #     if attrs['old_password'] == attrs['new_password']:
    #         raise serializers.ValidationError({
    #             'new_password': (
    #                 'New password must be different from '
    #                 'the old password.'
    #             )
    #         })

    #     return attrs
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
            'is_active',
            'created_at',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
            },
            'created_at': {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = User(**validated_data)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance