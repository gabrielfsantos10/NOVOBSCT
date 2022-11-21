"""
Essas visualizações não fazem nada além de fornecer membros do modelo BSCT 'simples'
definido como nomes de modelo padrão.
"""

# views que podem valer para vários apps, por exemplo o método "get_queryset", que definimos as permissões de cada tipo de usuário.
# contém as validações de criação, atualização e exclusão do projeto, onde mostra as mensagens após as ações


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin
from django.db.models import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin
from django.template import loader
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User


class CreateView(LoginRequiredMixin, generic.CreateView, SuccessMessageMixin):
    template_name = 'bsct/plain/form.html'
    success_message = 'Criado com sucesso!'

    # def post(self, request, *args, **kwargs):
    #     messages.success(self.request, self.success_message)
    #     return super(CreateView, self).post(request, *args, **kwargs)


class UpdateView(LoginRequiredMixin, generic.UpdateView, SuccessMessageMixin):
    template_name = 'bsct/plain/form.html'
    success_message = 'Atualizado com sucesso!'

    def teste(request):
        return render(request, 'form.html')

    # def post(self, request, *args, **kwargs):
    #     messages.success(self.request, self.success_message)
    #     return super(UpdateView, self).post(request, *args, **kwargs)


class ListFilterView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'bsct/plain/list.html'
    title = None
    personal_queryset = None

    def get_context_data(self, **kwargs):
        context = super(ListFilterView, self).get_context_data(**kwargs)

        # TODO - Tornar o tratamento abaixo dinâmico e tirar o hardcode
        if self.title:
            context['titulo'] = self.title
        try:
            if self.table_class.Meta.extra_content:
                context['extra_action'] = self.table_class.Meta.extra_content['extra_action']
                context['extra_button'] = self.table_class.Meta.extra_content['extra_button']
        except:
            pass
        return context


class ListView(LoginRequiredMixin, SingleTableView):
    template_name = 'bsct/plain/list.html'
    title = None


class DetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'bsct/plain/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        try:
            if self.request.META['HTTP_REFERER']:
                redirect_concluido = None
                if '/solicitacaotitular/' in self.request.META['HTTP_REFERER']:
                    redirect_concluido = '/solicitacaotitular'
                elif '/solicitacaointerna/' in self.request.META['HTTP_REFERER']:
                    redirect_concluido = '/solicitacaointerna'
                elif '/solicitacaoexterna/' in self.request.META['HTTP_REFERER']:
                    redirect_concluido = '/solicitacaoexterna'
                elif '/solicitacao/' in self.request.META['HTTP_REFERER']:
                    redirect_concluido = '/solicitacao'

                if redirect_concluido:
                    context['redirect_concluido'] = redirect_concluido

        except Exception as e:
            print(e)
            pass

        return context


class DeleteView(LoginRequiredMixin, generic.DeleteView, SuccessMessageMixin):
    template_name = 'bsct/plain/confirm_delete.html'
    success_message = 'Deletado com sucesso!'

    def post(self, request, *args, **kwargs):
        msg_sucess = True
        try:
            return self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
        except ProtectedError:
            msg_sucess = False
            template = loader.get_template('bsct/plain/cant_delete.html')
            context = {'object': self.object,
                       'cant_delete_msg': 'O registro não pôde ser excluído'}
            return HttpResponse(template.render(context, request))
        except Exception as e:
            msg_sucess = False
            messages.error(self.request, 'Falha na exclusão do registro: (' + str(e) + ')')
            template = loader.get_template('bsct/plain/cant_delete.html')
            context = {'object': self.object,
                       'cant_delete_msg': e}
            return HttpResponse(template.render(context, request))
        finally:
            if msg_sucess:
                messages.success(self.request, self.success_message)
