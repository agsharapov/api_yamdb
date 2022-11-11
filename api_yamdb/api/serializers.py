from rest_framework import serializers
from reviews.models import (Category, Genre, Title,
                            User, Review, Comment)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя «me» нельзя использовать.')
        return value


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя «me» нельзя использовать.')
        return value


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя «me» нельзя использовать.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Этот email уже использовался для регистрации.'
            )
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GetTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating',
        )
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=False)
    category = CategorySerializer(many=False, required=False)
    rating = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'score', 'text', 'author', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError(
                'Рейтинг должен быть целым числом от 0 до 10!'
            )
        return value

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        if (Review.objects.filter(author=author, title=title_id).exists()
           and self.context.get('request').method == 'POST'):
            raise serializers.ValidationError(
                'На одно произведение можно оставлять только один отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('review',)
