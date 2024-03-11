"""
   Serializer for Todo application API View. 
"""

from rest_framework import serializers
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, authenticate
from todo_app.models import Todo


class TodoSerializer(serializers.Serializer):
    """Serializer for todo object."""
    id = serializers.IntegerField(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    title = serializers.CharField()
    is_done = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        validated_data['updated_at'] = timezone.now()
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.updated_at = timezone.now()
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object."""
    todolist = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'todolist']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return account with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return the user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        account = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not account:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = account
        return attrs
