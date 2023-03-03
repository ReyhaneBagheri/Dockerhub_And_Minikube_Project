from flask import Flask ,request, jsonify
import os
from redis import Redis
import requests
#from dotenv import load_dotenv


Redis= Redis( host = 'myredis' , port = 6379)
app =Flask(__name__)
#load_dotenv('myenv.env')
#time_ = os.getenv('time_')
#port_= os.getenv('port_')
#ArzNmae=os.getenv('ArzNmae')
#time_ = os.environ.get('time_')
#port_= os.environ.get('port_')
#ArzNmae=os.environ.get('ArzNmae')

ENV_PORT = os.environ.get('ENV_PORT')
ENV_TIME = os.environ.get('ENV_TIME')
ENV_ARZNAME = os.environ.get('ENV_ARZNAME')
print(ENV_PORT)
print(ENV_TIME)
print(ENV_ARZNAME)
print(type(ENV_ARZNAME))


def checkexist(ENV_ARZNAME) :
    if Redis.get(ENV_ARZNAME) is None:
        return False
    return True
   

def getPrice():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    response = requests.get(url , params={'vs_currency': 'usd' , 'ids' : ENV_ARZNAME}).json()
    return response[0]['current_price']


def saveRedis(PRICE):
    Redis.set(ENV_ARZNAME,PRICE,ex=int(ENV_TIME)  )


@app.route('/' , methods=['GET'])
def test():
    if request.method == "GET":
        if checkexist(ENV_ARZNAME) == True :
            return jsonify({"ArzName": ENV_ARZNAME,"price": (Redis.get(ENV_ARZNAME)).decode('utf-8')})
        PRICE= getPrice()
        saveRedis(PRICE) 
        return jsonify({"ArzName": ENV_ARZNAME,"price": PRICE})

if __name__ =='__main__':
    
     app.run(debug=True ,host='0.0.0.0' , port=ENV_PORT)

    