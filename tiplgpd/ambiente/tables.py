import django_tables2 as tables

from tiplgpd.settings import DJANGO_TABLES2_TABLE_ATTRS
from .models import Area


class AreaTable(tables.Table):
    buttons = tables.TemplateColumn(
        template_name="table_columns/table_buttons.html", verbose_name="Ações", orderable=False, attrs={'class': "text-sm-end"}
    )

    class Meta:
        model = Area
        fields = ('id', 'nome', 'responsavel', 'segundo_responsavel', 'apelido', 'buttons')
        attrs = DJANGO_TABLES2_TABLE_ATTRS
