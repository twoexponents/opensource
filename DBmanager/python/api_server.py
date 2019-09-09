

import json
from database import DBHandler


from flask import Flask, jsonify, request
#from flask.ext.restful import Api, Resource, reqparse
from flask_restful import Api, Resource, reqparse
from flask_restful.utils import cors
#from flask.ext.restful.utils import cors
#from flask.ext.cors import CORS
from flask_cors import CORS

from modules.ssh import QoSHandler


app = Flask(__name__)
CORS(app)
api = Api(app)

config = json.load(open('./config.json', 'r'))

db_handler = DBHandler(config)


class UserAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()

    super(UserAPI, self).__init__()

  @cors.crossdomain(origin='*')
  def get(self, uid):
    users = []
    if uid != 'all':
      users = uid.split(',')

    resultset = db_handler.get_users(users)

    d = {}
    for item in resultset:
      d[item['uid']] = item

    return jsonify(d)

  @cors.crossdomain(origin='*')
  def post(self, uid):
    req = json.loads(request.data)
    d = {'uid':uid}
    if req is not None:
      d = {k:v for k, v in req.iteritems()}
    ret = db_handler.put_or_update_user(d)

    return 'Success' if ret else 'Fail'

  #@cors.crossdomain(origin='*')
  def put(self, uid):
    req = json.loads(request.data)
    print req
    ret = db_handler.put_or_update_user(req)

    return 'Success'

  @cors.crossdomain(origin='*')
  def delete(self, uid):
    ret = db_handler.delete_user(uid)

    return 'Success' if ret else 'Fail'


class QoSAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()

    super(QoSAPI, self).__init__()

  @cors.crossdomain(origin='*')
  def get(self, id):
    tp = request.args.get('type')

    aps = []
    if id != 'all':
      aps = id.split(',')

    resultset = db_handler.get_all_aps(aps)

    d = {}
    if tp is None or tp == "":
      for ap in resultset:
        try:
          h = QoSHandler(ap['sudoer_id'], ap['sudoer_passwd'], ap['ap_ip'])
          h.close()
        except Exception, e:
          continue

      for item in resultset:
        d[item['ap_ip']] = item

    elif tp == "class":
      for ap in resultset:
        try:
          h = QoSHandler(ap['sudoer_id'], ap['sudoer_passwd'], ap['ap_ip'])
          d[ap['ap_ip']] = h.inquiry_class(ap)
        except Exception, e:
          print e

    elif tp == "filter":
      classid = request.args.get('classid')

      for ap in resultset:
        try:
          h = QoSHandler(ap['sudoer_id'], ap['sudoer_passwd'], ap['ap_ip'])
          d[ap['ap_ip']] = h.inquiry_filter(ap, classid)
        except Exception, e:
          print e
          continue

    return jsonify(d)

  @cors.crossdomain(origin='*')
  def post(self, id):
    req = json.loads(request.data)
    d = {'id':id}
    if req is not None:
      d = {k:v for k, v in req.iteritems()}

    ret = db_handler.put_or_update_aps(d)
    """

    if d.has_key('classes'):
      classes = d['classes'] # form {'classid':{'rate':'1600Kbit'}}
      try:
        h = QoSHandler(d['sudoer_id'], d['sudoer_passwd'], d['ap_ip'])
        for cls in classes:
          ret = h.modify_class(d['ap_ip'], cls)
      except Exception, e:
        print e

    if d.has_key('filters'):
      filters = d['filters'] # {'filterid':{'classid':'1:5', 'dest_ip':'192.168.42.10'}}
      try:
        h = QoSHandler(d['sudoer_id'], d['sudoer_passwd'], d['ap_ip'])
        for flt in filters:
          ret = h.modify_filters(d['ap_ip'], flt)
      except Exception, e:
        print e
    """

    return 'Success' if ret else 'Fail'

  #@cors.crossdomain(origin='*')
  def put(self, id):
    req = json.loads(request.data)
    d = {}
    if req is not None:
      d = {k:v for k, v in req.iteritems()}

    ret = db_handler.put_or_update_aps(d)
    """

    if d.has_key('classes'):
      classes = d['classes'] # form {'classid':{'rate':'1600Kbit'}}
      try:
        h = QoSHandler(d['sudoer_id'], d['sudoer_passwd'], d['ap_ip'])
        for cls in classes:
          ret = h.add_class(d['ap_ip'], cls)
      except Exception, e:
        print e

    if d.has_key('filters'):
      filters = d['filters'] # {'filterid':{'classid':'1:5', 'dest_ip':'192.168.42.10'}}
      try:
        h = QoSHandler(d['sudoer_id'], d['sudoer_passwd'], d['ap_ip'])
        for flt in filters:
          ret = h.add_filters(d['ap_ip'], flt)
      except Exception, e:
        print e
    """

    return 'Success'

  @cors.crossdomain(origin='*')
  def delete(self, id):
    ret = db_handler.delete_aps(id)

    return 'Success' if ret else 'Fail'


api.add_resource(UserAPI, '/api/user/<string:uid>', endpoint='user')
api.add_resource(QoSAPI, '/api/qos/<string:id>', endpoint='qos')

#api.add_resource(UserListAPI, '/api/userlist/<string:uids>', endpoint='users')


@app.route('/')
def helloworld():
  return 'Hello World!'


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=config['api_server']['port'],
          debug=True)



