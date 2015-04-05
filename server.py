from flask import Flask,jsonify,request
from jsonschema import validate,ValidationError,SchemaError
import ConfigParser
from pymongo import MongoClient
import datetime

app = Flask(__name__)

@app.route("/")
def hello():
	return jsonify({'success':True,'message':"welcome ! use /get or /post"})

@app.route("/get",methods=['GET'])
def get():
	return jsonify(getData().process_request(request.json))

@app.route("/post",methods=['POST'])
def post():
	result = postData().process_request(request.json)
	return jsonify(result)

class getData:
	def process_request(self,request):
		dbserver = config.get('database','dbserver')
		dbport   = int(config.get('database','dbport'))
		try:
			client = MongoClient(dbserver,dbport)
			db = client[config.get('database','dbname')]
			posts = db['posts']
			result = posts.find({'isTaken':False}).sort('date',1).limit(1)
			doc = {}
			for r in result:
				doc = r
			if not doc:
				return {'success':False,'message':'No data to show'}
			posts.update({'_id':doc['_id']},{'$set':{'isTaken':True}})
			return {'success':True,'fileName':doc['fileName'],'fileContent':doc['fileContent']}
		except:
			return {'sucess':False,'message':'some error occured'}
		

class postData:
	def __init__(self):
		self.schema = {
			"title":"Input Message Schema",
			"type":"object",
			"properties":{
				"fileName":{
					"type":"string"
				},
				"fileContent":{
					"type":"string"
				}
			},
			"required":["fileName","fileContent"]
		}
	def process_request(self,request):
		try:
			validate(request,self.schema)
			if len(request['fileName'].strip()) == 0 or len(request['fileContent'].strip()) == 0:
				raise ValueError('fileName or fileContent cannot be Empty');
		except ValidationError as v:
			return {'success':False,'message':v.message}
		except SchemaError as s:
			return {'success':False,'message':s.message}
		except ValueError as e:
			return {'success':False,'message':e.message}

		dbserver = config.get('database','dbserver')
		dbport   = int(config.get('database','dbport'))
		try:
			client = MongoClient(dbserver,dbport)
			db = client[config.get('database','dbname')]
			posts = db['posts']
			posts.insert({
						'fileName':request['fileName'].strip(),
						'fileContent':request['fileContent'].strip(),
						'date':datetime.datetime.utcnow(),
						'isTaken':False
					})
		except:
			return {'sucess':False,'message':'some error occured'}
		return {'success':True,'message':'data added successfully'}
			
if  __name__ == "__main__":
	config = ConfigParser.ConfigParser()
	config.read("config.cf")
	app.debug = True
	app.run(port=5001)
