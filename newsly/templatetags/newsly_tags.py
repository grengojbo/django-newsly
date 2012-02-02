import datetime

from django.core.urlresolvers import reverse
from django import template

from newsly.models import News

register = template.Library()


class LatestNewsNode(template.Node):
    def __init__(self, varname, limit=1):
        self.varname = varname
        self.limit = limit
    
    def render(self, context):
        rs = News.published.all()[0:self.limit]
        if self.limit == 1:
            context[self.varname] = rs[0]
        else:
            context[self.varname] = rs[0:self.limit]
        return ''

@register.tag(name="get_latest_news")
def get_latest_news(parser, token):
    bits = token.contents.split()
    if len(bits) != 3 and len(bits) != 5:
        raise template.TemplateSyntaxError, "get_latest_news tag takes either two or four arguments"
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "first argument to the get_latest_news tag must be 'as'"
    if len(bits) == 5:
        if bits[3] != 'limit':
            raise template.TemplateSyntaxError, "third argument to the get_latest_news tag must be 'limit'"
        limit = bits[4]
    else:
        limit = 1
    try:
        limit = int(limit)
    except ValueError:
        raise template.TemplateSyntaxError, "Forth argument to the get_latest_news tag must an integer"

    return LatestNewsNode(bits[2], limit)
