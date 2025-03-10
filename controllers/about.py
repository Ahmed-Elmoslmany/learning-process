import http

class GetInformationAboutProject:
    def __init__(self, request):
        self._request = request
    
    @property
    def serialize(self):
        return _AboutProjectInformationSerializer
    
    @property
    def retriver(self):
        return _ProjectInformationRetriver('about.txt')
    
    def get_information(self):
        information_file = self.retriver.read_infomation_file()
        information_array = self.retriver.get_information_array(information_file)
        return _AboutProjectInformationSerializer(information_array).serialize(self._request.path), http.HTTPStatus.OK


class _AboutProjectInformationSerializer:
    def __init__(self, lines):
        self._lines = lines
        
    def serialize(self, path):
        information_object = {
            "path": path
        }
        for line in self._lines:
            raw = line.strip().replace('"', '').replace(" ", '').replace('-', ' ').split('=')
            information_object[raw[0]] = raw[1]
        return information_object
    
    
class _ProjectInformationRetriver:
    def __init__(self, file_name):
        self._file_name = file_name
        
    def read_infomation_file(self):
        file = open(self._file_name, 'r')
        return file
    
    def get_information_array(self, file):
        lines = []
        for line in file:
            lines.append(line)
        return lines
