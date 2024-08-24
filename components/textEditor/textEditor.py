from django_components import Component, register

@register('textEditor')
class textEditor(Component):
    template_name = './textEditor.html'