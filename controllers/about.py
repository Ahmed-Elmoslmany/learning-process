import http
import about

class GetInformationAboutProject:
    def __init__(self, request):
        self._request = request
    
    @property
    def serializer(self):
        return _AboutProjectInformationSerializer()
    
    def get_information(self):
        return self.serializer.serialize(self._request.path), http.HTTPStatus.OK


class _AboutProjectInformationSerializer: 
            
    def serialize(self, path):
        return {
            "path": path,
            "project": about.project,
            "package": about.package,
            "description": about.description,
            "copyright": about.copyright,
            "author": about.author,
            "author_email": about.author_email,
            "release": about.release,
            "build_number": about.build_number,
            "version": about.version,
        }
        