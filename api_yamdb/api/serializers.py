from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from titles.models import Category, Genre, Title
from reviews.models import Score, Review, Comment


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