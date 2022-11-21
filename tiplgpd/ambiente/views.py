from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def home_view(request):

    template = loader.get_template('home.html')

    titulo = 'TIPLGPD'
    conteudo = '<h1>Bem vindo ao TIPLGPD</h1>'
    conteudo += '<p>Plataforma de atendimento dedicada e especializada'
    conteudo += 'nos direitos dos titulares, cumprimento do requisito legal de '
    conteudo += 'transparência e facilidade de acesso.</p>'

    return HttpResponse(template.render({'titulo': titulo,
                                         'conteudo': conteudo,
                                         }, request))

def tabela_modal(request):
    template = loader.get_template('form_teste.html')

    return HttpResponse(template.render(), request)
    # return render(request, 'form.html')

def shortcuts_view(request):
    template = loader.get_template('shortcuts.html')
    return HttpResponse(template.render({'titulo': 'Shortcuts'}, request))


def help_view(request):
    template = loader.get_template('help.html')
    return HttpResponse(template.render({'titulo': 'Help',
                                         'conteudo': 'Help'}, request))


def sobre_view(request):
    template = loader.get_template('sobre.html')
    return HttpResponse(template.render({'titulo': 'Sobre...',
                                         'conteudo': 'Versão 1.0.1.141'}, request))
