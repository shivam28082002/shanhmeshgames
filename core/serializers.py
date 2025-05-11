from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Character, Skin, Purchase,UserCharater

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user



# serializers.py



class SkinSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Skin
        fields = ['id', 'name', 'price', 'image_url', 'is_unlocked']

    def get_is_unlocked(self, skin):
        user = self.context.get('user')
        if not user or user.is_anonymous:
            return False
        return Purchase.objects.filter(user=user, skin=skin).exists()

class SkinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skin
        fields = ['id', 'name', 'price', 'image_url', 'is_unlocked']



class CharacterSerializer(serializers.ModelSerializer):
    skins = SkinSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'name', 'description', 'skins']


class UserCharaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCharater
        fields = ['id', 'character', 'level', 'engry']