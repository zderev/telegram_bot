import requests
import pandas as pd
import json
import time

def parse_dict_for_payment(user_id, user_dict):
    amount = user_dict["amount"]
    task_link = user_dict["task_link"]
    task_type = user_dict["task_type"]
    url = """https://qiwi.com/payment/form/99?extra%5B%27account%27%5D=79998496829&amountInteger={0}&amountFraction=0&extra%5B%27comment%27%5D={1}&currency=643""".format(amount, user_id)
    return amount, task_link, url, task_type

def payment_history(qw_login, qiwi_token):
    api_access_token = qiwi_token
    my_login = qw_login
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token  
    parameters = {'rows': '20'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+my_login+'/payments', params = parameters)
    df = pd.DataFrame(json.loads(h.text)["data"])
    df['sum'] = df['sum'].apply(lambda x: x["amount"])
    df["date"] = pd.to_datetime(df["date"])
    df = df[["account", "date", "status", "comment", "sum", "type"]]
    df = df[df["type"] == "IN"]
    return df

def check_payments(user_id, qw_login, qiwi_token):
    df = payment_history(qw_login, qiwi_token)
    if df[(df.comment == str(user_id))
        & (df.status =="SUCCESS")].empty == False:
        return True
    else:
        return False

def _get_profile(api_access_token):
    s = requests.Session()
    s.headers['content-type']= 'application/json'
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token
    p = s.get('https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    return json.loads(p.text)



def send_p2p(api_access_token,to_qw,comment,sum_p2p):
    my_login = _get_profile(api_access_token)['authInfo']['personId']
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['Accept']= 'application/json'
    postjson = json.loads('{"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"},"comment":"'+comment+'","fields":{"account":""}}')
    postjson['id']=str(int(time.time() * 1000))
    postjson['sum']['amount']=sum_p2p
    postjson['sum']['currency']='643'
    postjson['fields']['account']=to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json=postjson)
    result = json.loads(res.text)
    try:
        if result['transaction']["state"]["code"] == 'Accepted':
            result = "OK"
            return result
        else:
        	 result = result['transaction']["state"]["code"]
    except Exception as e:
        return e