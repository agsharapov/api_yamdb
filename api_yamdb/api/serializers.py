from rest_framework import serializers
from reviews.models import (Category, Genre, Title, TitleGenre,
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
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'genre', 'category', 'description', 'rating'
        )
        model = Title

    def create(self, validated_data):
        self.initial_data._mutable = True
        genres = self.initial_data.pop('genre')
        cats = self.initial_data.pop('category')[0]
        self.initial_data._mutable = False
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.get_or_create(slug=genre)[0]
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        current_category = Category.objects.get_or_create(slug=cats)[0]
        title.category = current_category
        title.save()
        return title

    def update(self, instance, validated_data):
        self.initial_data._mutable = True
        if 'name' in self.initial_data:
            name = self.initial_data.pop('name')[0]
            self.instance.name = name
        if 'category' in self.initial_data:
            cats = self.initial_data.pop('category')[0]
            current_category = Category.objects.get_or_create(slug=cats)[0]
            self.instance.category = current_category
        self.initial_data._mutable = False
        self.instance.save()
        return self.instance

    def get_rating(self, obj):
        rate = Review.objects.filter(
            title_id=obj.id
        ).values_list('score', flat=True)
        if len(rate) == 0:
            rating = None
        else:
            rating = sum(rate) / len(rate)
        return rating


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
