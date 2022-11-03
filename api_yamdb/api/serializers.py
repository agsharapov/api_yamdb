from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title
from reviews.models import User, Review, Comment
from django.shortcuts import get_object_or_404

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
    genre = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Genre.objects.all()) #serializers.PrimaryKeyRelatedField #SlugRelatedField
    category = serializers.SlugRelatedField(many=True, slug_field='slug', queryset=Category.objects.all()) #serializers.PrimaryKeyRelatedField
    
    class Meta:
        fields = ('name','year', 'genre', 'category', 'description')
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name','slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name','slug',)
        model = Category



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
       read_only=True, slug_field='username')
   
    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]
            
    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError('Рейтинг должен быть целым числом от 0 до 10!')
        return value

    def validate(self, data):
        title_id = self.kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, pk=title_id)
        if (title.reviews.filter(author=author).exists()
           and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'На одно произведение можно оставлять только один отзыв!'
            )
        return data

    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
    