# A very simple Flask Hello World app for you to get started with...


from flask import Flask, request, redirect
from operator import itemgetter

import random
import json
import boto3

app = Flask(__name__)

AWSKEY = 'AKIAVRUVVOGIQRYMIFGG'
AWSSECRET = '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'
PUBLIC_BUCKET = 'ai55853n-web-public'
STORAGE_URL = 'http://ai55853n-web-public.s3-website.us-east-2.amazonaws.com'

def get_public_bucket():
    s3 = boto3.resource(service_name='s3', region_name='us-east-2',
    aws_access_key_id=AWSKEY,
    aws_secret_access_key=AWSSECRET)

    bucket = s3.Bucket(PUBLIC_BUCKET)
    return bucket

@app.route('/listfiles')
def listfiles():
    bucket = get_public_bucket()


    items = []
    for item in bucket.objects.all():
        items.append(item.key)


    return {'url':STORAGE_URL, 'items': items}


@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    bucket = get_public_bucket()
    file = request.files["file"]
    filename = file.filename
    bucket.upload_fileobj(file, filename)
    return {'results': 'ok'}



@app.route('/hello')
def hello():
    return '<h1><b>Carmine</b> says Hello!</h1>'

@app.route('/dice')
def dice():
    x = random.randint(1, 6)
    result = 'Your roll was <b>' + str(x) + '</b>'
    return result

@app.route('/pizza')
def pizza():
    pizzas = [
        {'name':'Plain', 'price':10.50},
        {'name':'Pepperoni', 'price':12.75},
        {'name':'Grandmas', 'price':14.00},
        {'name':'Meat Lovers', 'price':18.75}
        ]
    p = random.choice(pizzas)
    return p

@app.route('/add')
def add():
    a = request.args.get('a')
    b = request.args.get('b')
    total = int(a) + int(b)
    return 'I added those for you: ' + str(total)


@app.route('/catalog/<search>')
def catalog(search):
    f = open('/home/thunderlegend/mysite/data/courses.json')
    courses = json.load(f)
    f.close()

    result_list = []
    for c in courses:
        if c['number'].lower().startswith(search.lower()) or search.lower() in c['name'].lower():
            result_list.append(c)

    return { 'result':result_list }

@app.route('/apt/<search>/<beds>/<sort>')
def apt(search, beds, sort):
    f = open('/home/thunderlegend/mysite/data/apartments.json')
    apartments = json.load(f)
    f.close()

    result_list = []

    # filter
    for a in apartments:
        if search.lower() in a['title'].lower() or search.lower() in a['description'].lower():
            if a['beds'] >= int(beds):
                result_list.append(a)

    # Sort
    if sort == "1":
        result_list = sorted( result_list, key=lambda d: d['monthly rent'])

    elif sort == "2":
        result_list = sorted( result_list, key=itemgetter('monthly rent'), reverse=True)



    return { 'result':result_list }




@app.route('/seidenberg')
def seidenberg():
    return redirect('https://www.pace.edu/seidenberg')

@app.route('/account')
def account():
    logged_in = False

    if not logged_in:
        return redirect('/hello')

    return 'Hello You!'

