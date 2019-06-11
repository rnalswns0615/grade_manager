from flask import Flask, request
from flask_restful import Resource, Api, reqparse


import os
import re
import time
import sys
import json
import configparser
import logging
import datetime
import pandas as pd

GLOBAL_CONFIG = configparser.ConfigParser()
GLOBAL_CONFIG.read('../../server.config')

sys.path.insert(0, GLOBAL_CONFIG['PATH']['SERVER_SRC_PATH'])
from subprocess import Popen

from train import train
from export import export
from predict import do_inference
from accuracy import get_accuracy
from get import display_param, display_trainedmodel, display_model, display_embedding
from ver_manage import version_up
from delete import delete_param, delete_model, delete_embedding
sys.path.insert(0, GLOBAL_CONFIG['PATH']['PARAMETER_SRC_PATH'])
from build_params import make_train_param, make_predict_param
sys.path.insert(0, GLOBAL_CONFIG['PATH']['DATA_PROCESSING_SRC_PATH'])
from embedding import word_embedding, char_embedding
from data_processing import TensorflowConfig, MakeMarkerFile, check_marker_file, read_marker_file, validity_monthly_data, validity_daily_data

app = Flask(__name__)
api = Api(app)
state = {}
tf_model_server = [
    'voc_lev3_InternetFE_PstnFE',
    'voc_lev3_MobileFE',
    'voc_lev3_All',
    'pro_lev1_All'
]

params = {
    "PARAMS":  # parameters
    {
        "model_name": ("string", "MODEL_NAME", "Model name of the trained model."),
        "model_id": ("string", "MODEL_ID", "Model id of the trained model."),
        "model_dir": ("string", "MODEL_DIR", "Model directory of the trained model."),
        "input_date": ("string", "INPUT_DATE", "Date list to train model."),
    }
}
predict_params = {
    "PREDICT":
    {
        "who_train": ("string", "WHO_TRAIN", "Who made the trained data for prediction"),
        "model_id": ("string", "MODEL_ID", "Model id to using train"),
        "concurrency": ("int", "CONCURRENCY", "maximum number of concurrent inference requests"),
        "max_sentence_length": ("int", "MAX_SENTENCE_LENGTH", "maximum length of sentence"),
        "min_word_length": ("int", "MIN_WORD_LENGTH", "minimum characters of word"),
        "max_word_length": ("int", "MAX_WORD_LENGTH", "maximum characters of word"),
        "mecab_filters": ("string", "MECAB_FILTERS", "morphemes tags that remain"),
        "model_name": ("string", "MODEL_NAME", "model name"),
        "model_signature_name": ("string", "MODEL_SIGNATURE_NAME", "signature"),
        "batch_size": ("int", "BATCH_SIZE", "batch size"),
    },
}

def get_logger():
    """
    Args:
    Returns: logger instance for logging.
    """

    # initialize logger
    logger = logging.getLogger("serving")

    if len(logger.handlers) > 0:
        return logger

    logging.root.setLevel(level=logging.INFO)
    logger.setLevel('INFO')

    log_format = GLOBAL_CONFIG.get('LOGGING', 'LOG_FORMAT', raw=True)
    formatter = logging.Formatter(log_format)
    log_path = "{}/serving_{}.log".format(
        GLOBAL_CONFIG['PATH']['SERVING_LOG_PATH'],
        datetime.datetime.now().strftime('%Y%m%d'))
    file_handler = FileHandler(log_path)
    file_handler.setFormatter(formatter)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


class Predict(Resource):
    def __init__(self):
        pass
    def post(self):
        try:
            check_user_id = request.json['user_id']
            check_session_id = request.json['session_id']
            check_parameter_id = request.json['parameter_id']
            check_top_k = request.json['top_k']
            check_text = request.json['text']
            check_service_name = request.json['given']['service_name']
        except:
            return {"message" : "ok", "request_code": "400", "result" : "Errors in json format."}

        path_system = TensorflowConfig.get_path(
            request.json['parameter_id'], 'predict', 'system')
        path_user = TensorflowConfig.get_path(
            request.json['parameter_id'], 'predict', 'user')

        if os.path.exists(path_system) != True and os.path.exists(path_user) != True:
            return {"message" : "ok", "request_code": "400", "results" : "Missing required parameter error."}

        elif os.path.exists(path_system) and os.path.exists(path_user):
            return {"message" : "ok", "request_code": "400", "results" : "Duplicated parameters error."}

        elif os.path.exists(path_system):
            path = path_system

        elif os.path.exists(path_user):
            path = path_user

        else:
            return {"message" : "ok", "request_code": "400", "results" : "Duplicated parameters error."}

        try:
            if int(request.json['top_k']) not in range(1,11):
                return {"message" : "ok", "request_code": "400", "results" : "top_k should be 1<= k <=10"}
        except:
            return {"message" : "ok", "request_code": "400", "results" : "top_k should be 1<= k <=10"}


        if request.json['given']['service_name'] not in tf_model_server:
            return {"message" : "ok", "request_code": "400", "results" : "Not allowed tensorflow_model_server."}

        FLAGS = TensorflowConfig.parse_tf_config(predict_params, path)
        url =  GLOBAL_CONFIG['PREDICTING']['TENSORFLOW_MODEL_HOST'] + ':' + GLOBAL_CONFIG['PREDICTING']['TENSORFLOW_MODEL_PORT']

        try:
            prediction = do_inference(
                FLAGS, url, 1,
                request.json['text'],
                class_type=request.json['given']['service_name'].split('_')[0],
                model_spec_name=request.json['given']['service_name'],
                topk=int(request.json['top_k']),
                user_ip=request.json['user_id'])
            return prediction

        except:
            return {"message" : "ok", "request_code": "500", "results" : "Fail to classification."}


class Train(Resource):
    def __init__(self):
        pass
    def post(self):
        try:
            check_user_id = request.json['user_id']
            check_input_data = request.json['input_data']
            check_parameter_id = request.json['parameter_id']
        except:
            return {"message" : "ok", "request_code": "400", "result" : "Errors in json format."}

        global state

        """parameter validity check
        """
        path_system = TensorflowConfig.get_path(
            request.json['parameter_id'], 'train', 'system')
        path_user = TensorflowConfig.get_path(
            request.json['parameter_id'], 'train', 'user')

        if os.path.exists(path_system) != True and os.path.exists(path_user) != True:
            return {"message" : "ok", "request_code":"400", "results" : "Missing required parameter error."}
        elif os.path.exists(path_system) and os.path.exists(path_user):
            return {"message" : "ok", "request_code":"400","results" : "Duplicated parameters error."}
        elif os.path.exists(path_system):
            path = path_system
        elif os.path.exists(path_user):
            path = path_user
        else:
            return {"message" : "ok", "request_code":"400", "results" : "Check again the parameter id."}

        flags = TensorflowConfig.parse_tf_config(params, path)

        """date validity check
        """
        param_date_match = re.match('[0-9]{8}-[0-9]{8}', flags.input_date)
        date_match = re.match('[0-9]{8}-[0-9]{8}', request.json['input_data'])
        date_index = []

        if date_match:
            if int(request.json['input_data'].split("-")[0]) > int(request.json['input_data'].split("-")[1]):
                return {"message" : "ok", "request_code":"400", "results" : "Entered date is incorrect."}
            else:
                date_index = pd.date_range(request.json['input_data'].split("-")[0], request.json['input_data'].split("-")[1])

        elif param_date_match and not date_match:
            date_index = pd.date_range(flags.input_date.split("-")[0], flags.input_date.split("-")[1])
            print 'Entered date is incorrect so train with date in parameter.'
        else:
            return {"message" : "ok", "request_code":"400", "results" : "Entered date and date in parameter are incorrect."}

        date_list = date_index.strftime("%Y%m%d").tolist()

        for date in date_list:
            if len(date) == 8:
                if os.path.exists("{}/daily/PRE_DAILY_{}_001/data.txt".format(
                    GLOBAL_CONFIG['PATH']['PREPROCESSING_DATA_PATH'],
                    date)) != True:
                    return {"message" : "ok","request_code":"400", "results" : "Missing required storage error."}
            else:
                return {"message" : "ok", "request_code":"400", "results" : "Check input_data format.."}

        """load parameter
        """
        flags = TensorflowConfig.parse_tf_config(params, path)

        model_dir = "{}/{}".format(
            GLOBAL_CONFIG['PATH']['DATA_PATH'],
            flags.model_dir)

        model_path = "{}/{}/{}/trains".format(
            model_dir,
            flags.model_name,
            flags.model_id)

        """check model duplicated
        """
        if os.path.exists("{}/models_saved/system/{}/{}".format(
            GLOBAL_CONFIG['PATH']['DATA_PATH'],
            flags.model_name,
            flags.model_id)):
            text = "system/{}/{} already exist.".format(
                flags.model_name,
                flags.model_id)
            return {"message" : "ok", "request_code" : 400, "results" : text}
            
        if os.path.exists("{}/models_saved/user/{}/{}".format(
            GLOBAL_CONFIG['PATH']['DATA_PATH'],
            flags.model_name,
            flags.model_id)):
            text = "user/{}/{} already exist.".format(
                flags.model_name,
                flags.model_id)
            return {"message" : "ok", "request_code" : 400, "results" : text}

        """make trained_model directory
        """
        if not os.path.exists("{}/{}".format(model_dir, flags.model_name)):
            os.mkdir("{}/{}".format(model_dir, flags.model_name))
        if not os.path.exists(
            "{}/{}/{}".format(model_dir, flags.model_name, flags.model_id)):
            os.mkdir("{}/{}/{}".format(model_dir, flags.model_name, flags.model_id))
        if not os.path.exists(model_path):
            os.mkdir(model_path)

        """check status
        """
        if len(state) == 0:
            state['start_path'] = "{}/start_training.status".format(model_path)
            state['finish_path'] = "{}/finish_training.status".format(model_path)
            MakeMarkerFile("{}/start_training.status".format(model_path), 'start_training')
            Popen(['python', os.path.join(GLOBAL_CONFIG['PATH']['SERVER_SRC_PATH'], 'train.py'), path, ' '.join(date_list), request.json['user_id']])
            return {"message" : "ok", "request_code":"200", "results" : "Start training."}

        else:
            if 'accuracy.status' in state['start_path']:
                return {"message" : "ok", "request_code":"200", "results" : "Check with finish_accuracy button. (still getting accuracy)'"}
            else:
                return {"message" : "ok", "request_code":"200", "results" : "Check with finish_train button. (still training model)'"}


class GetTrainStatus(Resource):
    def __init__(self):
        pass
    def post(self):
        try:
            check_user_id = request.json['user_id']
        except:
            return {"message" : "ok", "request_code": "400", "result" : "Errors in json format."}
        global state
        if len(state) < 1:
            return {"message" : "ok", "request_code":"200", "results" : "Server is free, can do training the model or getting accuracy."}
        if check_marker_file(state['start_path']) and check_marker_file(state['finish_path']):
            text = read_marker_file(state['finish_path'])
            os.remove(state['start_path'])
            os.remove(state['finish_path'])
            state = {}
            return {"message" : "ok", "request_code":"200", "results" : text}
        if check_marker_file(state['start_path']):
            if 'accuracy.status' in state['start_path']:
                return {"message" : "ok", "request_code":"200", "results" : "Try again later. (still getting accuracy)"}
            else:
                return {"message" : "ok", "request_code":"200", "results" : "Try again later. (still training model)"}

        return {"message" : "ok", "request_code":"400", "results" : "Not expectation error"}


class Accuracy(Resource):
    def __init__(self):
        pass
    def post(self):
        try:
            check_user_id = request.json['user_id']
            check_parameter_id = request.json['parameter_id']
        except:
            return {"message" : "ok", "request_code": "400", "result" : "Errors in json format."}
        global state
        path_system = TensorflowConfig.get_path(
            request.json['parameter_id'], 'predict', 'system')
        path_user = TensorflowConfig.get_path(
            request.json['parameter_id'], 'predict', 'user')

        if os.path.exists(path_system) != True and os.path.exists(path_user) != True:
            return {"message" : "ok", "request_code":"400", "results" : "Missing required parameter error."}
        elif os.path.exists(path_system) and os.path.exists(path_user):
            return {"message" : "ok", "request_code":"400", "results" : "Duplicated  parameters error."}
        elif os.path.exists(path_system):
            path = path_system
        elif os.path.exists(path_user):
            path = path_user
        else:
            return {"message" : "ok", "request_code":"400", "results" : "Duplicated  parameters error."}

        flags = TensorflowConfig.parse_tf_config(predict_params, path)
        model_path = "{}/{}/{}/{}/trains".format(
            GLOBAL_CONFIG['PATH']['MODEL_DATA_PATH'],
            flags.who_train,
            flags.model_name,
            flags.model_id)

        if len(state) == 0:
            state['start_path'] = "{}/start_accuracy.status".format(model_path)
            state['finish_path'] = "{}/finish_accuracy.status".format(model_path)
            if check_marker_file(state['start_path']):
                os.remove(state['start_path'])
            if check_marker_file(state['finish_path']):
                os.remove(state['finish_path'])
            MakeMarkerFile("{}/start_accuracy.status".format(model_path), 'start getting accuracy')
            Popen(['python', os.path.join(GLOBAL_CONFIG['PATH']['SERVER_SRC_PATH'], 'accuracy.py'), path, request.user_id])
            return {"message" : "ok", "request_code":"200", "results" : "Start getting accuracy."}
        else:
            if 'accuracy.status' in state['start_path']:
                return {"message" : "ok", "request_code":"200", "results" : "Check with finish_accuracy button. (still getting accuracy)."}
            else:
                return {"message" : "ok", "request_code":"200", "results" : "Check with finish_train button. (still training model)."}


class GetAccuracyStatus(Resource):
    def __init__(self):
        pass
    def post(self):
        try:
            check_user_id = request.json['user_id']
        except:
            return {"message" : "ok", "request_code": "400", "result" : "Errors in json format."}
        global state
        if len(state) < 1:
            return {"message" : "ok", "request_code":"400", "results" : "Server is free, can do training the model or getting accuracy."}

        if check_marker_file(state['start_path']) and check_marker_file(state['finish_path']):
            text = read_marker_file(state['finish_path'])
            os.remove(state['start_path'])
            os.remove(state['finish_path'])
            state = {}
            return {"message" : "ok", "request_code":"200", "results" : text}
        if check_marker_file(state['start_path']):
            if 'accuracy.status' in state['start_path']:
                return {"message" : "ok", "request_code":"200", "results" : "Try again later. (still getting accuracy)"}
            else:
                return {"message" : "ok", "request_code":"200", "results" : "Try again later. (still training model)"}

        return {"message" : "ok", "request_code":"400", "results" : "Not expectation error."}


api.add_resource(Predict, '/classifier/predict')
api.add_resource(Train, '/classifier/train')
api.add_resource(GetTrainStatus, '/classifier/get_train_status')
api.add_resource(Accuracy, '/classifier/accuracy')
api.add_resource(GetAccuracyStatus, '/classifier/get_accuracy_status')

if __name__== '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

