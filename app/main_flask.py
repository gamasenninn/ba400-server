from flask import Flask,make_response,redirect,request
import tpcl_maker as tpcl
import json
import uuid
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/test')
def test():
    return app.send_static_file('test-tpcl.html')




@app.route('/tpclmaker',methods=["GET","POST"])
@cross_origin(supports_credentials=True)
def maketpcl():

    if request.method == "GET":
        return redirect('/tpclmaker/print_conf_ip')
    elif request.method == "POST":
        d = request.json
        ret = tpcl.tpcl_maker(d)
        if ret:
            with open('tpcl_send.log','r',encoding='utf-8') as f:
                response = f.read()
                return {"data":response}
        return {}

@app.route('/tpclmaker/<jsonc_file>')
@cross_origin(supports_credentials=True)
def maketpcl_file(jsonc_file):

    conf = tpcl.read_jsonc_file(jsonc_file+".jsonc")
    ret = tpcl.tpcl_maker(conf)
    if ret:
        with open('tpcl_send.log','r',encoding='utf-8') as f:
            response = f.read()
            return f"<pre>{response}</pre>"

@app.route('/tpclmaker/status/<jsonc_file>')
@cross_origin(supports_credentials=True)
def get_status(jsonc_file):

    #return jsonc_file
    conf = tpcl.read_jsonc_file(jsonc_file+".jsonc")
    data =  tpcl.analize_status(conf)
    return json.dumps(data, indent=2, ensure_ascii=False)

@app.route('/tpclmaker/status',methods=["POST"])
@cross_origin(supports_credentials=True)
def get_status_post():
        d = request.json
        data =  tpcl.analize_status(d)
        return json.dumps(data, indent=2, ensure_ascii=False)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8100, debug=True)