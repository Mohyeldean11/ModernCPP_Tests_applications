import requests
# payload ={
#     'username': "mohy.badawy" ,
#     'password' : "testing"
# }

# r = requests.post('https://httpbin.org/post',data=payload)
r = requests.get('https://httpbin.org/basic-auth/mohy/testing',auth=('mohy','testing'),timeout=3)

print(r)
