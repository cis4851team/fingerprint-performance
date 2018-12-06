import json

results_file = open('./results.csv')
results = results_file.read()
results_file.close()

result_split = results.split('\n')

# creates a dictionary of dictionaries
parsed = {}
for line in result_split:
    if ';' not in line:
        continue

    [key, _value] = line.split(';')

    try:
        value = json.loads(_value)
        if len(value) <= 0:
            continue

        parsed[key] = value
    except:
        continue


# combine entries by cookie (because one person is identified by a cookie_id)
entries_by_cookie_id = {}
for [hit_id, value] in parsed.items():
    cookie_id = value.get('cookie_id')
    if not cookie_id:
        continue

    fingerprints_for_this_cookie_id = entries_by_cookie_id.get(cookie_id, [])
    current_fingerprints = value.get('fingerprints', [])

    for fingerprint in current_fingerprints:
        fingerprints_for_this_cookie_id.append(fingerprint)

    entries_by_cookie_id[cookie_id] = fingerprints_for_this_cookie_id
print('amount of unique cookie_ids:', len(entries_by_cookie_id))

cookie_id_with_reliable_fingerprints = {}
for [cookie_id, fingerprints] in entries_by_cookie_id.items():
    if len(fingerprints) < 0:
        continue
    first_fingerprint = fingerprints[0]

    for fingerprint in fingerprints:
        if fingerprint != first_fingerprint:
            continue

    cookie_id_with_reliable_fingerprints[cookie_id] = first_fingerprint
print('amount of unique cookie_ids with reliable fingerprints:',
      len(cookie_id_with_reliable_fingerprints))

fingerprint_to_cookie_ids = {}
for [cookie_id, fingerprint] in cookie_id_with_reliable_fingerprints.items():
    cookies = fingerprint_to_cookie_ids.get(fingerprint, [])

    cookies.append(cookie_id)

    fingerprint_to_cookie_ids[fingerprint] = cookies

print('amount of unique fingerprints', len(fingerprint_to_cookie_ids))

for [fingerprint, cookies] in fingerprint_to_cookie_ids.items():
    if len(cookies) > 1:
        print('collision:', fingerprint, cookies)

# results after running this file:
# amount of unique cookie_ids: 118
# amount of unique cookie_ids with reliable fingerprints: 118
# amount of unique fingerprints 117
# collision: 7f9b1489c64692464628c2bef2b141ac65e2f110 ['0fc0a489fbb74aae8f31be242e674e4f', '9ce1d9e253914fceb9351e13b45384d7']