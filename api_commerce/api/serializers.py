from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user_new = User(
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        user_email = self.validated_data['email']
        if User.objects.filter(email=user_email).exists():
            raise serializers.ValidationError({"emai_error": "User with this email already exist"})
        if password != password2:
            raise serializers.ValidationError({"password": "password must match"})
        user_new.set_password(password)
        user_new.email = user_email
        user_new.save()
        return user_new
