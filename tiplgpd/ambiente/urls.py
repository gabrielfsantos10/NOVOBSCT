from django.urls import path, include, re_path
from bsct.urls import URLGenerator
from tiplgpd import settings
from . import views, models

# Ambiente
from .filters import AreaFilter
from .tables import AreaTable
from bsct.views import ListFilterView

bsct_patterns = URLGenerator(models.Area,
                             table_class=AreaTable,
                             filterset_class=AreaFilter).get_urlpatterns(paginate_by=settings.DEFAULT_PAGINATION_COUNT)

urlpatterns = [
    # URLGenerator
    path('', include(bsct_patterns)),
    path('', views.home_view, name='home'),
    # path('teste', views.tabela_teste, name='teste'),
    path('area/tabela_modal', views.tabela_modal, name='tabela_modal'),

    # path('area', ListFilterView.as_view(), name='list_area_teste'),

    # Shortcuts
    path('shortcuts', views.shortcuts_view, name='shortcuts'),
    path('sobre', views.sobre_view, name='sobre'),
    path('help', views.help_view, name='help'),
]
