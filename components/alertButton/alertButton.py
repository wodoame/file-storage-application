from django_components import Component, register

@register('alertButton')
class alertButton(Component):
    template_name = './alertButton.html'
    class Media: 
        pass