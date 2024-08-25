from django_components import register, Component

@register('toast')
class Toast(Component): 
    template_name = './toast.html'
    
    def get_context_data(self, *args,  **kwargs):
        return kwargs