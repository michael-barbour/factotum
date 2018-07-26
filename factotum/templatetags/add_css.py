# This code adapted from https://medium.com/@sumitlni/paginate-properly-please-93e7ca776432

from django import template

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
