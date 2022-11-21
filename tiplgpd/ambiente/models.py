from django.contrib.auth.models import User
from django.db import models
from bsct.models import BSCTModelMixin
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError


# Area
class Area(BSCTModelMixin, models.Model):
    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['id']

    # Fields
    nome = models.CharField('Nome da Área', max_length=100, unique=True)
    responsavel = models.ForeignKey(User, verbose_name='Responsável', on_delete=models.PROTECT)
    segundo_responsavel = models.ForeignKey(User, verbose_name='Segundo Responsável', related_name='segundo',
                                            null=True, on_delete=models.PROTECT, default=None)
    apelido = models.CharField('Apelido da Área', max_length=10, default='', unique=True)
    tempo_resposta = models.IntegerField('Tempo de Resposta (horas)', default=72)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True, null=True)

    def __str__(self):
        return '%s' % self.nome

    def clean(self):
        if self.responsavel == self.segundo_responsavel:
            raise ValidationError('O primeiro e o segundo reponsável não podem ser os mesmos')

    @classmethod
    def get_allowed_fields(cls):
        return ['id', 'nome', 'responsavel', 'segundo_responsavel', 'apelido', 'tempo_resposta']
