from django_components import Component, register
from core.models import Folder
from core.utils import getSVG

@register('files')
class Files(Component): 
    """ A components that renders the files and folders """
    template_name = './files.html'
    
    def get(self, request, username, id):
        folder = Folder.objects.get(id=id)
        files = folder.files.all()
        subFolders = folder.sub_folders.all()
        combined = list(files) + list(subFolders)
        combined.sort(key=lambda x: x.created)
        combined = [
            {
                'name': item.name, 
                'icon': getSVG('folder') if item.isFolder() else getSVG(item.extension), # * could have used isinstance(item, Folder) but that doesn't matter
                'openurl': f"/{username}/{item.id}/" if item.isFolder() else "#",
                'downloadurl': '#' if item.isFolder() else f'/download/{item.id}/' 
            } for item in combined
        ]
        return self.render_to_response(context={'filesAndFolders': combined}) 