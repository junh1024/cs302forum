#http://gomputor.wordpress.com/2008/09/27/search-replace-multiple-words-or-characters-with-python/

from django import template
register = template.Library()

# define our method
@register.filter
def myreplace(value):
    for i, j in dic.iteritems():
        value = value.replace(i, j)
    return value
myreplace.is_safe = True

dic = {'[b]':'<b>', '[i]':'<i>', '[u]':'<u>','[/b]':'</b>', '[/i]':'</i>', '[/u]':'</u>'}


