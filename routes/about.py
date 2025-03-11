from app import app
import controllers.about as ab

@app.route('/about', methods=['GET'])
def about():
    return ab.GetAboutProjectInformationController().serialize()