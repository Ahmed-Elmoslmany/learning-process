from app import app
import controllers.about as ab
import flask as fl

@app.route('/about', methods=['GET'])
def about():
    return ab.GetInformationAboutProject(fl.request).get_information()