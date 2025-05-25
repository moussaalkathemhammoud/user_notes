from rest_framework import serializers
from .models import MyUser,Note


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(email=validated_data['email'], password=validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','text','created_at','color']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
