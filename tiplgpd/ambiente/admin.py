from django.contrib import admin

from ambiente.models import Area


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    model = Area
    list_display = ['id', 'nome', 'responsavel', 'apelido']
    search_fields = ['nome']
