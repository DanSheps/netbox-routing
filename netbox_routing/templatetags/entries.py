from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag()
def get_entry_url(method, instance, return_url):
    url = (
        f'plugins:{instance._meta.app_label}:{instance._meta.model_name}entry_{method}'
    )

    if not return_url:
        return_url = instance.get_absolute_url()
    return reverse(
        url,
        query={f'{instance._meta.model_name}': instance.pk, 'return_url': return_url},
    )
