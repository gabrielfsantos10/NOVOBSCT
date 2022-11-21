# Utiliza o modelo de "BSCTModelMixin" para criar outros modelos, além de utilizar o padrão "models.Model"
from django.shortcuts import render
# criação de url de forma rápida
#     def get_create_url(cls):
#         return 'registro_dados'

# Usa como métodos em baixo da declaração dos campos, como exemplo o: "get_allowed_fields"
# -------
# DÚVIDA - get_allowed_fields - para campos permitidos?

from django.urls import reverse


class BSCTModelMixin(object):
    """
    Fornece uma implementação padrão para os métodos de definição de URL.

    Os nomes de URL devem seguir o formato <lowercasemodelname>_<action>.
    """

    def __init__(self, *args, **kwargs):
        """
        Define o prefixo para os nomes de URL.
        """
        super(BSCTModelMixin, self).__init__(*args, **kwargs)

        self.bsct_view_prefix = self.__class__.__name__.lower()

    def get_absolute_url(self):
        """
        Retorna o URL da página de detalhes dessa instância.
        """
        return reverse(
            '%s_detail' % self.bsct_view_prefix, kwargs={'pk': self.pk}
        )

    def get_delete_url(self):
        """
        Retorna o URL da página de exclusão dessa instância.
        """
        return reverse(
            '%s_delete' % self.bsct_view_prefix, kwargs={'pk': self.pk}
        )

    def get_update_url(self):
        """
        Retorna o URL da página de atualização dessa instância.
        """
        return reverse(
            '%s_update' % self.bsct_view_prefix, kwargs={'pk': self.pk})

    @classmethod
    def get_create_url(cls):
        """
        Retorna o URL da página de criação do modelo.
        """
        return reverse('%s_create' % cls.__name__.lower())

    def get_list_url(self):
        """
        Retorna o URL da página de listagem do modelo.
        """
        # Este costumava ser um método de classe, porém só é chamado em
        # templates no # contexto de uma instância de modelo, tornando uma instância
        # método mais prático. (Evita ter que criar templatetags para
        # chamar o método de classe na classe de instância. )
        return reverse('%s_list' % self.bsct_view_prefix)

    @classmethod
    def get_allowed_fields(cls):
        """
        Retorna a lista de campos de modelo CRUD-expansíveis.

        Caso contrário, o padrão é a palavra-chave "__all__", aceita pelo
        método django.forms.modelform_factory
        """
        return "__all__"
