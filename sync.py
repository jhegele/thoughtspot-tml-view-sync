from os import environ
import requests
import json

TS_USERNAME = environ.get('TS_USERNAME')
SECRET_KEY = environ.get('TS_SECRET_KEY')
TS_HOST = environ.get('TS_HOST')
TS_LIVEBOARD_GUID_DEV = environ.get('TS_LIVEBOARD_GUID_DEV')
TS_LIVEBOARD_GUID_PROD = environ.get('TS_LIVEBOARD_GUID_PROD')

# die if username is not set
assert TS_USERNAME is not None
# die if secret key is not set
assert SECRET_KEY is not None
# die if host is not set
assert TS_HOST is not None
# die if liveboard guids are not set
assert TS_LIVEBOARD_GUID_DEV is not None
assert TS_LIVEBOARD_GUID_PROD is not None

def get_tml(liveboard_guid, token):
    # get dev TML (no views)
    payload = {
        "metadata": [
            {
                "identifier": liveboard_guid,
                "type": "LIVEBOARD"
            }
        ],
        "export_associated": False,
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{TS_HOST}/api/rest/2.0/metadata/tml/export"
    r = requests.post(url, headers=headers, json=payload);
    res = r.json()
    # parse TML as JSON
    tml = json.loads(res[0]['edoc'])
    return tml

# get auth token
print('Authenticating...')
auth_payload = {
    "username": TS_USERNAME,
    "validity_time_in_sec": 300,
    "secret_key": SECRET_KEY
}
url = f"{TS_HOST}/api/rest/2.0/auth/token/full"
r = requests.post(url, json=auth_payload)

res = r.json()
token = res['token']

# get dev TML (no views)
print('Getting TML (dev)...')
tml_dev = get_tml(TS_LIVEBOARD_GUID_DEV, token)

# get prod TML (w/ views)
print('Getting TML (prod)...')
tml_prod = get_tml(TS_LIVEBOARD_GUID_PROD, token)
views = tml_prod['liveboard']['views']

# update dev TML
print("Syncing TML Views (Prod -> Dev)...")
tml_dev['guid'] = tml_prod['guid']
# copy views from prod TML to dev TML
tml_dev['liveboard']['views'] = views
# preserve name of prod liveboard
tml_dev['liveboard']['name'] = tml_prod['liveboard']['name']

# push updated TML to prod (preserve views)
print("Pushing updated TML...")
import_payload = {
    "metadata_tmls": [json.dumps(tml_dev)]
}
import_headers = {
    "Authorization": f"Bearer {token}"
}
url = f"{TS_HOST}/api/rest/2.0/metadata/tml/import"
r = requests.post(url, headers=import_headers, json=import_payload)
print("Done!")
print(f"Response status: {r.status_code}")