import requests
import json
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import os
from helpers.text2img import draw
from helpers.vinamilk import generate_vinamilk_img
# Vãi cả soi ạ =)))))))))))
app = Flask(__name__)
api = Api(app)


class Draw(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('prompt',
                                 type=str,
                                 help="Đây là cái promt và NÓ KHÔNG THỂ RỖNG",
                                 required=True,
                                 location='args')
        self.parser.add_argument('key',
                                 type=str,
                                 help="Key truy cập",
                                 required=True,
                                 location='args')
        self.parser.add_argument('height',
                                 type=int,
                                 help="Key truy cập",
                                 location='args')
        self.parser.add_argument('width',
                                 type=int,
                                 help="Key truy cập",
                                 location='args')

    def get(self, model_type):
        if model_type not in [1, 2, 3, 4, 5, 6, 7]:
            return {'status': 'error', 'message': 'Model không tồn tại'}, 400
        if model_type == 1:
            model_id = os.environ['MIDJOURNEY']
        elif model_type == 2:
            model_id = os.environ['CYBER_COLOSCK']
        elif model_type == 3:
            model_id = os.environ['ULTRA']
        elif model_type == 4:
            model_id = os.environ['STABLE-DIFFUSION']
        elif model_type == 6:
            model_id = os.environ['COUNTERFEIT']
        elif model_type == 7:
            model_id = 'meinamix'
        else:
            model_id = os.environ['ULTIMATEJOURNEY']
        args = self.parser.parse_args()
        key = args['key']

       
        return draw(args['prompt'], model_id, args['height'], args['width'])


class Introduce(Resource):

    def get(self):
        return [{
            'model_id': [1, 2, 3, 4, 5, 6, 7]
        }, {
            'model': [{
                1: 'MidJourney'
            }, {
                2: "Cyber-Colosck"
            }, {
                3: "Ultra Realistic Colosck Promax"
            }, {
                4: "STABLE-DIFFUSION"
            }, {
                5: "UltimateJourney"
            }, {
                6: "Counterfeit"
            }, {
                7: "meinamix"
            }]
        }]


class VinamilkName(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'name',
            type=str,
            help="Đây là cái tên",
            required=True,
            location='args',
        )
        self.parser.add_argument('ltext',
                                 type=str,
                                 help="Đây là dòng chữ bên trái",
                                 required=True,
                                 location='args')
        self.parser.add_argument('rtext',
                                 type=str,
                                 help="Đây là dòng chữ bên phải",
                                 required=True,
                                 location='args')

    def get(self):
        args = self.parser.parse_args()
        if len(args['name']) < 4:
            return {
                'status': 'Error',
                'problem': 'name phải tối thiểu 4 ký tự'
            }, 404
        name = args['name'].upper()
        return {
            'status': 'success',
            'url': generate_vinamilk_img(name, args['ltext'], args['rtext'])
        }
@app.route('/')
def home():
    return "<h1>I'm alive</h1>"

api.add_resource(Draw, '/v0.5/<int:model_type>')
api.add_resource(VinamilkName, '/v0.5/vinamilk')
api.add_resource(Introduce, '/v0.5/introduce')

