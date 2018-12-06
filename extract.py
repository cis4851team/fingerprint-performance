import redis
import os
import uuid

r = redis.from_url(os.environ.get('REDIS_URL'))
csv = open('./results.csv', 'w')
csv.write('key;result\n')
for key in r.keys():
  result = r.get(key)
  key_decoded = key.decode('UTF-8')
  result_decoded = result.decode('UTF-8')
  csv.write(f'{key_decoded};{result_decoded}\n')
csv.close()
