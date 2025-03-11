import http
import about

class GetAboutProjectInformationController: 
    def serialize(self):
        return {
            "project": about.project,
            "package": about.package,
            "description": about.description,
            "copyright": about.copyright,
            "author": about.author,
            "author_email": about.author_email,
            "release": about.release,
            "build_number": about.build_number,
            "version": about.version,
        }, http.HTTPStatus.OK
        