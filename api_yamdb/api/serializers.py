from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title
from reviews.models import User, Score, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'bio', 'first_name', 'last_name',
        )


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'bio', 'first_name', 'last_name',
        )


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField
    category = serializers.PrimaryKeyRelatedField

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


# class ScoreSerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = '__all__'
#         model = Score

class ReviewSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(
    #    read_only=True, slug_field='username'
    #)
    class Meta:
        fields = '__all__'
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    #author = serializers.SlugRelatedField(
    #    read_only=True, slug_field='username'
    #)

    class Meta:
        fields = '__all__'
        model = Comment