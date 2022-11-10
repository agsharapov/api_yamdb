import django_filters
from reviews.models import Genre, Title


class GenreFilter(django_filters.FilterSet):
    make = django_filters.ModelChoiceFilter(
        field_name='Genre__slug',
        to_field_name='slug',
        queryset=Title.objects.all()
    )

    class Meta:
        model = Genre
        fields = ('genre',)


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
