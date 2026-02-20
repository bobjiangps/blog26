from django import template
import re


register = template.Library()


@register.filter('replace_tags')
def replace_tags(content):
    pattern = re.compile(r'<.*?>')
    return re.sub(pattern, '', content)
