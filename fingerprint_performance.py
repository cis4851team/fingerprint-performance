import os
import datetime
import uuid
import json
import redis
from flask import Flask, Markup, make_response, request

r = redis.from_url(os.environ.get("REDIS_URL"))
app = Flask(__name__)

fingerprinter_file = open('./fingerprinter.js')
fingerprinter = fingerprinter_file.read()
fingerprinter_file.close()

fingerprint2_file = open('./libs/fingerprint2.min.js')
fingerprint2 = fingerprint2_file.read()
fingerprint2_file.close()

object_hash_file = open('./libs/object_hash.min.js')
object_hash = object_hash_file.read()
object_hash_file.close()

token_secret = '79cc1cc1a7bf4642bd33dfea73ead6b9'

styles = '''
    html { font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif }
    body { display: flex; }
    .container { margin: auto; }
    .submit {
        font-size: 2.6rem;
        font-weight: bold;
        display: block;
    }
    .loader {
        font-size: 2rem;
        font-weight: bold;
    }
'''


def create_webpage(token):
    return Markup(f'''
        <html>
            <head>
                <title>Fingerprinting Experiment</title>
                <style>{styles}</style>
            </head>
            <body>
                <div class="container">
                    <h1>Fingerprinting Experiment</h1>
                    <div class="loader"></div>
                    <script>window.token = '{token}';</script>
                    <script>{fingerprint2}</script>
                    <script>{object_hash}</script>
                    <script>{fingerprinter}</script>
                </div>
            </body>
        </html>
    ''')


@app.route('/<token>')
def fingerprint_performance(token):
    token_result = r.get(token)
    if not token_result:
        return ('', 404)

    response = make_response(create_webpage(token))
    response.headers.set('Content-Type', 'text/html')

    cookie_id = request.cookies.get('cookie_id')
    if not cookie_id:
        cookie_id = uuid.uuid4().hex
        response.set_cookie('cookie_id',  cookie_id)

    return response


@app.route('/fingerprints', methods=['POST'])
def fingerprints():
    result = request.get_json()
    cookie_id = request.cookies.get('cookie_id')
    token = result['token']
    fingerprints = result['fingerprints']

    token_result = r.get(token)
    if not token_result:
        return ('', 404)

    value = json.dumps({
        'time': datetime.datetime.now().isoformat(),
        'fingerprints': fingerprints,
        'cookie_id': cookie_id,
    })

    r.set(token, value)

    return ('', 204)


@app.route('/validate/<token>', methods=['POST'])
def validate(token):
    result = r.get(token)

    if not result:
        return ('', 404)
    else:
        return ('', 204)


@app.route('/token/<token>', methods=['POST'])
def token(token):
    '''
    creates a token
    '''

    secret = request.args.get('secret')
    if not secret:
        return ('', 400)

    if secret != token_secret:
        return ('', 403)

    r.set(token, '{ }')
    return ('', 204)
