from django_components import Component, register

@register('window')
class Window(Component):
    template_name = './window.html'