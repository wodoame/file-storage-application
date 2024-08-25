from typing import Any, Dict
from django_components import register, Component

@register('toast')
class Toast(Component): 
    template_name = './toast.html'
    
    def get_context_data(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        result = kwargs
        print(result)
        return result