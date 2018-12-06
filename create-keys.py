import redis
import os
import uuid

r = redis.from_url(os.environ.get("REDIS_URL"))
csv = open('./tokens.csv', 'w')
csv.write('website_url\n')
for i in range(500):
  token = uuid.uuid4().hex
  csv.write(f'https://fingerprinter-experiment.herokuapp.com/{token}\n')
  r.set(token, '{ }')
csv.close()
