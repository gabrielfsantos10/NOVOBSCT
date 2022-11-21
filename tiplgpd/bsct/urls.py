# Utiliza-se na criação das urls em "ambiente", por exemplo.
# bsct_patterns = URLGenerator(models.Area,
#                              table_class=AreaTable,
#                              filterset_class=AreaFilter).get_urlpatterns(paginate_by=settings.DEFAULT_PAGINATION_COUNT)

# Na criação das urls, usamos a classe "URLGenerator" e o método "__init__" para passarmos alguns parâmetros necessários.
# nome do modelo, tabela, classse de filtro
# .get_urlpatterns nas urls de "Ambiente", serviram apenas para setar a quantidade padrão de paginação do site = 15

#     URLGenerator
#     path('', include(bsct_patterns)) - Desta forma dinamicamente conseguimos definir as urls

from django.urls import re_path, reverse_lazy
from bsct import views as bsct_views
from django.forms import modelform_factory

class URLGenerator(object):
    """
    Constrói e retorna URLs CRUD para visualizações BSCT genéricas para um determinado modelo.
    Os nomes de URL seguem o padrão:
        <nome do modelo em minúsculas>_<ação>
        - ``lowercasemodelname_detail``: Para o DetailView.
        - ``lowercasemodelname_create``: Para o CreateView.
        - ``lowercasemodelname_list``..: Para o ListView.
        - ``lowercasemodelname_update``: Para o UpdateView.
        - ``lowercasemodelname_delete``: Para o DeleteView.
    """

    def __init__(self, model, table_class=None, filterset_class=None, form_class=None,
                 queryset = None, bsct_view_prefix=None, extra_context=None, title=None, personal_queryset=None):
        """
        Internalize the model and set the view prefix.
        """
        self.model = model
        self.table_class = table_class
        self.filterset_class = filterset_class
        self.form_class = None
        self.queryset = queryset
        self.personal_queryset = personal_queryset
        self.bsct_view_prefix = bsct_view_prefix or model.__name__.lower()
        self.set_form_class(form_class)
        self.extra_context = extra_context
        self.title = title

    def set_form_class(self, form_class=None):
        """
        Sets the form class to be used by the create and update views.
        """
        if form_class:
            self.form_class = form_class
        else:

            # fields = self.model._meta._get_fields(reverse=False)
            fields = self.model.get_allowed_fields()

            self.form_class = modelform_factory(
                self.model,
                fields=fields
                # fields = '__all__'
            )

    def get_create_url(self, form_class=None, **kwargs):
        """
        Generate the create URL for the model.
        """
        form_class = form_class if form_class else self.form_class

        return re_path(
            r'%s/create/?$' % self.bsct_view_prefix,
            bsct_views.CreateView.as_view(
                model=self.model,
                form_class=form_class,
                **kwargs
            ),
            name='%s_create' % self.bsct_view_prefix,
        )

    def get_update_url(self, form_class=None, **kwargs):
        """
        Generate the update URL for the model.
        """
        form_class = form_class if form_class else self.form_class

        return re_path(
            r'%s/update/(?P<pk>\d+)/?$' % self.bsct_view_prefix,
            bsct_views.UpdateView.as_view(
                model=self.model,
                form_class=form_class,
                **kwargs
            ),
            name='%s_update' % self.bsct_view_prefix,
        )

    def get_list_url(self, **kwargs):
        """
        Generate the list URL for the model.
        """
        if self.filterset_class is None:
            return re_path(
                r'%s/(list/?)?$' % self.bsct_view_prefix,
                bsct_views.ListView.as_view(
                    model=self.model,
                    table_class=self.table_class,
                    queryset = self.queryset,
                    personal_queryset=self.personal_queryset,
                    title = self.title,
                    **kwargs
                ),
                name='%s_list' % self.bsct_view_prefix,)
        else:
            return re_path(
                r'%s/(list/?)?$' % self.bsct_view_prefix,
                bsct_views.ListFilterView.as_view(
                    model=self.model,
                    table_class=self.table_class,
                    filterset_class=self.filterset_class,
                    queryset = self.queryset,
                    personal_queryset=self.personal_queryset,
                    title=self.title,
                    **kwargs
                ),
                name='%s_list' % self.bsct_view_prefix,)

    def get_delete_url(self, **kwargs):
        """
        Generate the delete URL for the model.
        """
        return re_path(
            r'%s/delete/(?P<pk>\d+)/?$' % self.bsct_view_prefix,
            bsct_views.DeleteView.as_view(
                model=self.model,
                success_url=reverse_lazy('%s_list' % self.bsct_view_prefix),
                **kwargs
            ),
            name='%s_delete' % self.bsct_view_prefix,
        )

    def get_detail_url(self, **kwargs):
        """
        Generate the detail URL for the model.
        """
        return re_path(
            r'%s/(?P<pk>\d+)/?$' % self.bsct_view_prefix,
            bsct_views.DetailView.as_view(
                model=self.model, **kwargs
            ),
            name='%s_detail' % self.bsct_view_prefix,
        )

    def get_urlpatterns(self, crud_types='crudl', paginate_by=10):
        """
        Gere toodo o URL definido para o modelo e retorne como um objeto padrão.
        Tipos CRUD específicos podem estar no argumento de string crud_types especificado, onde:
            'c' - Refere-se ao tipo Criar CRUD
            'r' - Refere-se ao tipo CRUD de leitura/detalhe
            'u' - Refere-se ao tipo de atualização/edição CRUD
            'd' - Refere-se ao tipo Excluir CRUD
            'l' - Refere-se ao tipo de lista CRUD
        """
        urlpatterns = []
        if 'c' in crud_types:
            urlpatterns.append(self.get_create_url())
        if 'r' in crud_types:
            urlpatterns.append(self.get_detail_url())
        if 'u' in crud_types:
            urlpatterns.append(self.get_update_url())
        if 'l' in crud_types:
            urlpatterns.append(self.get_list_url(paginate_by=paginate_by))
        if 'd' in crud_types:
            urlpatterns.append(self.get_delete_url())

        return urlpatterns
