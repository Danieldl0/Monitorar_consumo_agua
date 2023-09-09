from rest_framework import serializers
from django.contrib.auth.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
    )
    senha = serializers.CharField(
        source="password",
        required=True
    )
    nome = serializers.CharField(
        source="first_name",
        required=True
    )
    sobrenome = serializers.CharField(
        source="last_name",
        required=False
    )

    class Meta:
        model =  User
        fields = ("username", "email", "senha", 'nome', 'sobrenome',)
    

    def validate(self, attrs):
        username = attrs.get('username')

        if User.objects.filter(
            username=username
        ).exists():
            raise serializers.ValidationError(
                {
                    "username": "Já existe um usuario cadastrado com este username"
                }
            )


        return super().validate(attrs)

    def create(self, validated_data):
        senha = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if senha is not None:
            instance.set_password(senha)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(
        source="password",
        required=True
    )
    username = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username', 'senha'
        )
    
    def validate(self, attrs):
        senha = attrs.get('password')
        username = attrs.get('username')

        user = User.objects.filter(
            username=username,
        ).first()

        if not user:
            raise serializers.ValidationError(
                {
                    "username": "Usuario não cadastrado"
                }
            )

        if not user.check_password(senha):
            raise serializers.ValidationError(
                {
                    "senha": "Senha incorreta"
                }
            )

        return super().validate(attrs)

    def create(self, validated_data):
        instance = User.objects.filter(
            username=validated_data.get('username'),
        ).first()
        return instance
