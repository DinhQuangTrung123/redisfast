import redis 
r = redis.Redis(host='localhost', port=6379, db=1)

brokerred = redis.Redis(host='localhost', port=6379, db=0)
bob_p = brokerred.pubsub()
# subscribe to classical music



Producer = redis.Redis(host='localhost', port=6379, db=0)
# publish new music in the channel epic_music
# Producer.publish('Order', 'Order 1')

# redisconsumes

# data = {'api_dev_key':API_KEY,
#         'api_option':'paste',
#         'api_paste_code':source_code,
#         'api_paste_format':'python'
# }

# import requests
# requests.get(url)
# request.post()

# # sending post request and saving response as response object
# r = requests.post(url = API_ENDPOINT, data = data)