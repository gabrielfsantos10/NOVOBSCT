import django_filters
from django_filters import rest_framework as filters

from .models import Area


class AreaFilter(filters.FilterSet):
    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')

    class Meta:
        model = Area
        fields = ('id', 'nome', 'responsavel', 'apelido')
