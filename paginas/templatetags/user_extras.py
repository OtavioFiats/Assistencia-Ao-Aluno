from django import template

register = template.Library()


@register.filter
def has_attr(obj, attr_name):
    """Retorna True se o objeto tiver o atributo (sem levantar exceção).

    Usado para checar relacionamentos OneToOne (ex: request.user.aluno) sem
    que o template quebre quando o objeto não existir.
    """
    try:
        return hasattr(obj, attr_name) and getattr(obj, attr_name) is not None
    except Exception:
        return False
