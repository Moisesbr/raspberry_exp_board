from bottle import route, run, template, get, post, request, Response
from bottle import HTTPResponse
import json
import RPi.GPIO as GPIO


my_token = '2e52d3eb834e09f30509fcf4837478f207e71f59'

dic_pins = {"input0":17,"input1":18,"input2":27,"input3":22,"input4":23,"input5":24,"input6":25,"input7":4}
input0 = 17
input1 = 18
input2 = 27
input3 = 22
input4 = 23
input5 = 24
input6 = 25
input7 = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(input0,GPIO.IN) #GPIO0
GPIO.setup(input1,GPIO.IN) #GPIO1
GPIO.setup(input2,GPIO.IN) #GPIO2
GPIO.setup(input3,GPIO.IN) #GPIO3
GPIO.setup(input4,GPIO.IN) #gpio4
GPIO.setup(input5,GPIO.IN) #GPIO5
GPIO.setup(input6,GPIO.IN) #GPIO6
GPIO.setup(input7,GPIO.IN) #GPIO7
GPIO.setwarnings(True)
print GPIO.VERSION

def verify_auth_token(token):
	try:
		if my_token == token:
			return True
		else:
			return False
	except:
		return False


@route('/input/state', method='POST')
def sensores_staus():
   token = request.forms.get('token')
   valid_token = verify_auth_token(token)
   if valid_token == True:
      try:
         sensores = return_state_inputs()
         #theBody = json.dumps({'200': 'ok'})
         return HTTPResponse(status=200, body=sensores)
      except:
         theBody = json.dumps({'500': 'Error'})
         return HTTPResponse(status=200, body=theBody)
   else:
      theBody = json.dumps({'401': 'Unauthorized'})
      return HTTPResponse(status=401, body=theBody)

def return_state_inputs():
   temp_array = []
   temp_array.append(GPIO.input(dic_pins["input0"]))
   temp_array.append(GPIO.input(dic_pins["input1"]))
   temp_array.append(GPIO.input(dic_pins["input2"]))
   temp_array.append(GPIO.input(dic_pins["input3"]))
   temp_array.append(GPIO.input(dic_pins["input4"]))
   temp_array.append(GPIO.input(dic_pins["input5"]))
   temp_array.append(GPIO.input(dic_pins["input6"]))
   temp_array.append(GPIO.input(dic_pins["input7"]))
   json_sensor_dic = {'inputs': {'input_state': temp_array}}
   return json.dumps(json_sensor_dic, indent=4)


run(host='0.0.0.0', port=9001)