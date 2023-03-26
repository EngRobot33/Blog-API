from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from ..models import User
from ..services.register import register
from ..validators import validator_numbers, validator_letters, validator_special_chars, validator_length


class RegisterApi(APIView):
    class RegisterInputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=255)
        password = serializers.CharField(max_length=255,
                    validators=[
                        validator_numbers,
                        validator_letters,
                        validator_special_chars,
                        validator_length,
                    ])
        confirm_password = serializers.CharField(max_length=255)

        def validate_username(self, username):
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Username already taken!")
            return username

        def validate(self, attrs):
            if not attrs.password or not attrs.confirm_password:
                raise serializers.ValidationError("You should set a password!")
            if attrs.password != attrs.confirm_password:
                raise serializers.ValidationError("Confirm password is not equal to password!")

    class RegisterOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'created_at', 'updated_at', )

    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request):
        serializer = self.RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                username=serializer.validated_data.get('username'),
                password=serializer.validated_data.get('password'),
            )
        except Exception as ex:
            return Response(data=f'Database Error: {ex}', status=status.HTTP_400_BAD_REQUEST)

        return Response(data=self.RegisterOutputSerializer(user).data, status=status.HTTP_201_CREATED)
