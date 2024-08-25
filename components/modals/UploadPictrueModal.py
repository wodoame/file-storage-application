from django_components import register, Component

@register('UploadPictureModal')
class UploadPictureModal(Component): 
    template_name = './UploadPictureModal.html'
    
