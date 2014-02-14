#coding:utf-8
from flask import Flask, request
from google import Google
import urllib2
import json
app = Flask(__name__)

@app.route("/query")
def query():
    job = request.args['job']
    
    lat = request.args['lat']
    lng = request.args['lng']
    city = get_city(lat, lng)
    print city
    
    rs = Google.search(urllib2.quote((u'%s %s 招聘' % (city, job,)).encode('utf-8')), append_url = '&tbs=qdr:w')
    return json.dumps({'result': [{"name": x.name, "email": x.email, "link":x.link} for x in rs]})

@app.route("/get_email")
def get_email():
    link = request.args['link']
    return json.dumps({'result': Google.parse_email(link)})
    


def get_city(lat, lng):
    url = 'http://api.map.baidu.com/geocoder?output=json&location=' + lat + ',%20' + lng + '&key=37492c0ee6f924cb5e934fa08c6b1676' 
    js = json.loads(urllib2.urlopen(url).read())
    return js['result']['addressComponent']['city']

if __name__ == "__main__":
    app.run(debug = True)
