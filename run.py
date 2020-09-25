import os
import gc
import uuid

from flask import Flask, request, redirect, url_for, send_file, session
import matplotlib.pyplot as plt

from app import config
from app.appsetting.AppSetting import AppSetting
from app.lib.CFound.CentroidImage import CentroidImage
from app.lib.ImageServer.ImageServer import ImageServer
from app.lib.util.util import callWithNonNoneArgs, getName, ClearFile
from app.lib.MaskDetection.MaskGalaxy import MaskGalaxy, InferenceConfig
import app.lib.mrcnn.model as modellib

from skimage.io import imsave, imread
from mrcnn import visualize

app = Flask(__name__)
#app.debug = True

appSet = AppSetting(os.getcwd())

MODEL_DIR = os.path.join(appSet.Config['modelos_dir'])
WEIGHTS_PATH = os.path.join(MODEL_DIR, appSet.Config['file_Weight'])

config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference",config=config,model_dir=MODEL_DIR)
model.load_weights(WEIGHTS_PATH, by_name=True)
model.keras_model._make_predict_function()


@app.route("/")
def hello():  
    return "Hola, Hello, Hallo!"

@app.route('/getgalaxy')
def getGalaxy():
    _ra = request.args.get('ra')
    _dec = request.args.get('dec')
    _scale = request.args.get('scale')
    _width = request.args.get('width')
    _height = request.args.get('height')
    _server = request.args.get('server')
    _return = request.args.get('ret')
    if (_ra is None) or (_dec is None):
        return 'falta RA o DEC'

    try:
        #appSet = AppSetting()
        IS = ImageServer(appSet.getConfig())
        MD = MaskGalaxy(appSet.getConfig())
        image = callWithNonNoneArgs(IS.getImage,Souce=_server,RA=_ra,DEC=_dec,SCALE=_scale,WIDTH=_width,HEIGHT=_height)
        CF = CentroidImage(image)
        r=MD.Detection(image,model)
        gc.collect()
        PathImage = os.path.join(appSet.getRoot(),appSet.getElem('images_folder'))
        PathCatalog = os.path.join(appSet.getRoot(),appSet.getElem('catalog_folder'))
        ClearFile(appSet.getElem('seconds_delete'),PathImage,PathCatalog)

        if (_server is None):
            _server="skyserver"
        if(_return=='image'):
            FileNameImage = getName(_ra,_dec,_server,appSet.getElem('image_name'))
            visualize.display_results(image, r['rois'], r['masks'], r['class_ids'], scores=r['scores'], show_mask=False,display_img=False,save_dir=PathImage,img_name=FileNameImage)
            return send_file(os.path.join(PathImage,FileNameImage), mimetype='image/jpeg')
        else:
            FileNameCatalog = getName(_ra,_dec,_server,appSet.getElem('catalog_name'))
            df = CF.find_ListCentroid(r)
            PathAndFile = os.path.join(PathCatalog,FileNameCatalog)
            CF.CreateCatalog(df,r, PathAndFile)
            return send_file(PathAndFile, mimetype='text/dat')
    except Exception as error:
    	return repr(error)    

@app.route('/getimage')
def getImage():
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

        image = callWithNonNoneArgs(IS.getImage,Souce=_server,RA=_ra,DEC=_dec,SCALE=_scale,WIDTH=_width,HEIGHT=_height)

        pathFile = os.path.join(os.path.abspath(appSet.getElem('images_folder')),_FileName)
        imsave(pathFile, image)
        return send_file(pathFile, mimetype='image/jpeg')
    except Exception as error:
    	return repr(error+"- parte dos")

if __name__ == "__main__":  
    app.run(port=8080, debug=False)