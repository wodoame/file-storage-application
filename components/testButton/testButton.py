from django_components import Component, register

@register('testButton')
class testButton(Component):
    template_name = './testButton.html'
    
    def get(self, request):
        return self.render_to_response()
    
    class Media: 
        pass