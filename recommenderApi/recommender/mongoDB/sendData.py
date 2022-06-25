from recommenderApi.imports import dt, requests, json, load, dump
from recommenderApi.settings import API_KEY_SECRET, MONGODB_UPDATE_TRAINING_TIME

def send_date(time: dt):
    url = MONGODB_UPDATE_TRAINING_TIME
    vars = load(open('recommenderApi/vars.pkl', 'rb'))
    vars['time'] = time
    dump(vars, open('recommenderApi/vars.pkl', 'wb'))
    payload = json.dumps({"date": time.isoformat()})
    headers = {
        'x-api-key': API_KEY_SECRET,
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print("Update training time: ", response.status_code == 200)