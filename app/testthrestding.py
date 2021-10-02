from threading import Thread
import threading
import time
# from server.redisfastapi.apiredis import *
import requests
import json

headers = {'Content-Type': 'application/json'}

def puptesting(product):
    # i=0
    data={
        "product":product,  
    }
    print(data)
    # print()
    # Producer.publish('Order', 'Order 1')
    H = requests.post(url ="http://localhost:5000/order/", data=json.dumps(data) , headers =  {'Content-Type': 'application/json'})
    print(H)

    # print("hahaha")
    # while i<5:
    #     print("hahaha")
    #     i=i+1

try:
    listla=[]
    t = time.time()
    for i in range(0,8):
        t1 = threading.Thread(target=puptesting,args=(str(i),))    
        listla.append(t1)
        t1.start()
    for a in listla:
        a.join()
    # t1.join()
	# t2.start()
    # t2 = threading.Thread(target=puptesting1)
	# t1.join()

	# t2.join()
    print ("done in ", time.time()- t)
except:
    print ("error")



# data={
#         "product":"product" 
#     }

# requests.post("http://localhost:5000/order/")
# H = requests.post(url ="http://localhost:5000/order/", data = data)

# request.post()

# data = {'api_dev_key':API_KEY,
#         'api_option':'paste',
#         'api_paste_code':source_code,
#         'api_paste_format':'python'}
  
# # sending post request and saving response as response object
# r = requests.post(url = API_ENDPOINT, data = data)
