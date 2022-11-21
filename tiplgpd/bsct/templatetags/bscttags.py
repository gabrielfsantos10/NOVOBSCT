# Conseguimos ao usar essas funções, retornar links como Bootstrap
# Funções que retornam nomes comuns (verbose_name)/nome original, como model

from django.core import serializers
from django.template import Library

register = Library()


# -------------------------
# Template Tags
# -------------------------

# CDN Resources
# -------------------------

def netdna_css(path):
    """
    Returns a link to the named NetDNA-hosted CSS resource.
    """
    return '//netdna.bootstrapcdn.com/%s' % path


def netdna_js(path):
    """
    Returns a link to the named NetDNA-hosted JavaScript resource.
    """
    return '//netdna.bootstrapcdn.com/%s' % path


@register.simple_tag
def bootstrap_js_cdn(version='3.1.1'):
    """
    Returns a link to a CDN-hosted Bootstrap minified JS file.
    """
    return netdna_js("bootstrap/%s/js/bootstrap.min.js" % version)


@register.simple_tag
def bootstrap_cdn(version='3.1.1'):
    """
    Returns a link to a CDN-hosted Bootstrap minified CSS file.
    """
    return netdna_css(
        'bootstrap/%s/css/bootstrap.min.css' % version
    )


@register.simple_tag
def bootswatch_cdn(theme, version='3.1.1'):
    """
    Returns a link to the named CDN-hosted Bootstrap Swatch theme.
    """
    return netdna_css(
        "bootswatch/%s/%s/bootstrap.min.css" % (version, theme.lower())
    )


# Verbose name retrievers
# -------------------------

@register.simple_tag
def get_verbose_name(instance):
    """
    Returns the verbose name for a model.
    """
    return instance._meta.verbose_name


@register.simple_tag
def get_verbose_name_plural(instance):
    """
    Returns the verbose pluralized name for a model.
    """
    return instance._meta.verbose_name_plural


# @register.simple_tag
@register.filter
def check_bsct_view_prefix(instance):
    """
    Returns the verbose pluralized name for a model.
    """
    teste = 1
    return True


# Pagination Helpers
# -------------------------

@register.simple_tag
def append_querystring(request, exclude=None):
    """
    Returns the query string for the current request, minus the GET parameters
    included in the `exclude`.
    """
    exclude = exclude or ['page']

    if request and request.GET:
        amp = '&amp;'
        return amp + amp.join(
            ['%s=%s' % (k, v)
             for k, v in request.GET.items()
             if k not in exclude]
        )

    return ''


# Filters
# -------------------------
@register.filter
def get_type(value):
    type_name = type(value)
    return type_name


@register.filter
def get_detail(instance):
    """
    Returns a dictionary of the models fields and values.

    If the method '<field>_detail' or verbose_name is defined, its value is used as the
    displayed value for the field.
    """
    fields = instance._meta.get_fields()
    details = {}
    allowed_fields = instance.get_allowed_fields()

    for field in fields:

        if allowed_fields == "__all__" or field.name in allowed_fields:
            detail_method = getattr(instance, '%s_detail' % field.name, None)
            verbose = getattr(field, 'verbose_name', None)
            value = getattr(instance, field.name, None)

            if field.is_relation:
                # Skipping model relations for now
                relation_verbose = getattr(field.related_model._meta, 'verbose_name')
                if getattr(field, 'multiple', False):
                    rset = getattr(instance, '%s_set' % field.name)
                    value = [i for i in rset.all()]
                if relation_verbose:
                    details[verbose] = value
                else:
                    details[field.name] = value
            elif field.choices:
                try:
                    choices = field.choices
                    option = field.choices[int(value)-1]
                    details[verbose] = option[1]
                except Exception as e:
                    details[field.name] = value
            elif detail_method:
                details[detail_method()] = value
            elif verbose:
                details[verbose] = value
            else:
                details[field.name] = value

    return details


@register.filter
def get_model_name(instance):
    model_name = instance._meta.verbose_name_plural
    return model_name
