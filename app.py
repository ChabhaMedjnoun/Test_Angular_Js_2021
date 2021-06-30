from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.interventioData

@application.route("/addintervention",methods=['POST']) 
def addintervention():
    try:
        json_data = request.json['info']
        libelleInt = json_data['libelle']
        desciptionInt = json_data['desciption']
        NomInt = json_data['NomInt']
        lieu = json_data['lieu']
        dateInt = json_data[' date']

        db.interventions.insert_one({
            'libelle':libelleInt,'desciption':desciptionInt,'NomInt':NomInt,'lieu':lieu,' date': dateInt
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
def showinterventionList():
    return render_template('list.html')

@application.route('/getintervention',methods=['POST'])
def getintervention():
    try:
        interventionId = request.json['id']
        intervention = db.interventions.find_one({'_id':ObjectId(interventionId)})
        interventionDetail = {
                'libelle':intervention['libelle'],
                'desciption':intervention['desciption'],
                'NomInt':intervention['NomInt'],
                'lieu':intervention['lieu'],
                'date':intervention['date'],
                'id':str(intervention['_id'])
                }
        return json.dumps(interventionDetail)
    except Exception, e:
        return str(e)

@application.route('/updateintervention',methods=['POST'])
def updateintervention():
    try:
        interventionInfo = request.json['info']
        interventionId = interventionInfo['id']
        libelle = interventionInfo['libelle']
        desciption = interventionInfo['desciption']
        NomInt = interventionInfo['NomInt']
        lieu = interventionInfo['lieu']
        date = interventionInfo['date']

        db.interventions.update_one({'_id':ObjectId(interventionId)},{'$set':{'libelle':libelle,'desciption':desciption,'NomInt':NomInt,'lieu':lieu,'date':date}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getinterventionList",methods=['POST'])
def getinterventionList():
    try:
        interventions = db.interventions.find()
        
        interventionList = []
        for intervention in interventions:
            print intervention
            interventionItem = {
                    'libelle':intervention['libelle'],
                    'desciption':intervention['desciption'],
                    'NomInt':intervention['NomInt'],
                    'lieu':intervention['lieu'],
                    'date':intervention['date'],
                    'id': str(intervention['_id'])
                    }
            interventionList.append(interventionItem)
    except Exception,e:
        return str(e)
    return json.dumps(interventionList)

@application.route("/execute",methods=['POST'])
def execute():
    try:
        interventionInfo = request.json['info']
        desciption = interventionInfo['desciption']
        NomInt = interventionInfo['NomInt']
        lieu = interventionInfo['lieu']
        command = interventionInfo['command']
        isRoot = interventionInfo['isRoot']
        
        env.host_string = NomInt + '@' + desciption
        env.lieu = lieu
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK',message=resp)
    except Exception, e:
        print 'Error is ' + str(e)
        return jsonify(status='ERROR',message=str(e))

@application.route("/deleteintervention",methods=['POST'])
def deleteintervention():
    try:
        interventionId = request.json['id']
        db.interventions.remove({'_id':ObjectId(interventionId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.run(host='127.0.0.1')

