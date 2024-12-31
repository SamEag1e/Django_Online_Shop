from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, *url_names):
    """
    Returns 'active' if the current URL name matches one of the given URL names.
    """
    current_url_name = context.request.resolver_match.url_name
    return "active" if current_url_name in url_names else ""
