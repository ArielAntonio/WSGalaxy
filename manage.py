import os
from flask_script import Manager
from flask import request, redirect, url_for, send_file
from app.lib.ImageServer.ImageServer import ImageServer
#from app.lib.MaskDetection.MaskGalaxy import MaskGalaxy
#from app import blueprint
from app.appsetting.AppSetting import AppSetting
import uuid


from app import create_app

app = create_app('dev')
#app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/getgalaxy')
def getGalaxy():
    _pathImage = "imagenes"
    _FileName = str(uuid.uuid4().hex)+".png"
    _ra = request.args.get('ra')
    _dec = request.args.get('dec')
    _scale = request.args.get('scale')
    _width = request.args.get('width')
    _height = request.args.get('height')
    _server = request.args.get('server')
    if (_ra is None) or (_dec is None):
        return 'falta RA o DEC'

    try:
        appSet = AppSetting()
        IS = ImageServer(appSet.getConfig())
        #MD = MaskGalaxy(AppSetting.getConfig())
        image = IS.getImage(RA=_ra,DEC=_dec)
        #r = MD.Detection(image, test=False)
        return print("print")
    except Exception as error:
    	return repr(error)


if __name__ == '__main__':
    manager.run()
    #app.run()