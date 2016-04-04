from bottle import route, run, template, get, post, request, Response
from bottle import HTTPResponse
import json
import smbus

bus = smbus.SMBus(1) 	# For revision 1 Raspberry Pi, change to bus = smbus.SMBus(1) for revision 2.
address = 0x20 			# I2C address of MCP23017
bus.write_byte_data(0x20,0x00,0x00) # Set all of bank A to outputs 
bus.write_byte_data(0x20,0x01,0x00) # Set all of bank B to outputs

my_token = '2e52d3eb834e09f30509fcf4837478f207e71f59'

dic_pins = {"relay1":0,"relay2":1,"relay3":2,"relay4":3,"relay5":4,"relay6":5,"relay7":6,"relay8":7,"relay9":0,"relay10":1, "transistor1":3, "transistor2":2, "transistor3":4}
#Classe para criar objetos json
class Simple_Json_Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def verify_auth_token(token):
	try:
		if my_token == token:
			return True
		else:
			return False
	except:
		return False

@route('/relay/transistor_on_off', method='POST')
def transistor():
   transistor_name = request.forms.get('transistorname')
   state = request.forms.get('state')
   token = request.forms.get('token')
   valid_token = verify_auth_token(token)
   if valid_token == True:
      if transistor_name == 'transistor1' or transistor_name == 'transistor2' or transistor_name == 'transistor3':
         if state == "high":
            print "aqui"
            high_rele(dic_pins[transistor_name],"b")
            print dic_pins[transistor_name]
            theBody = json.dumps({'200': transistor_name}) # you seem to want a JSON response
            return HTTPResponse(status=200, body=theBody)
         elif state == "low":
            low_rele(dic_pins[transistor_name],"b")
            theBody = json.dumps({'200': transistor_name}) # you seem to want a JSON response
            return HTTPResponse(status=200, body=theBody)
         else:
            theBody = json.dumps({'412': "Precondition Failed"}) # you seem to want a JSON response
            return HTTPResponse(status=412, body=theBody)
      else:
         theBody = json.dumps({'412': "Precondition Failed"}) # you seem to want a JSON response
         return HTTPResponse(status=412, body=theBody)
   else:
      theBody = json.dumps({'401': 'Unauthorized'}) # you seem to want a JSON response
      return HTTPResponse(status=401, body=theBody)

@route('/relay/toogle_relay', method='POST')
def toogle():
	relay_name = request.forms.get('relayname')
	token = request.forms.get('token')
	valid_token = verify_auth_token(token)
	if valid_token == True:
		if relay_name == 'relay1' or relay_name == 'relay2' or relay_name == 'relay3' or relay_name == 'relay4' or relay_name == 'relay5' or relay_name == 'relay6' or relay_name == 'relay7' or relay_name == 'relay8':
			tooglerelay_func(dic_pins[relay_name],"a")
		if relay_name == 'relay9' or relay_name == 'relay10':
			tooglerelay_func(dic_pins[relay_name],"b")
		theBody = json.dumps({'200': relay_name}) # you seem to want a JSON response
		return HTTPResponse(status=200, body=theBody)
	else:
		theBody = json.dumps({'401': 'Unauthorized'}) # you seem to want a JSON response
		return HTTPResponse(status=401, body=theBody)

@route('/relay/on_off', method='POST')
def on_off():
	relay_name = request.forms.get('relayname')
	token = request.forms.get('token')
	state = request.forms.get('state')
	valid_token = verify_auth_token(token)
	if valid_token == True:
		if relay_name == 'relay1' or relay_name == 'relay2' or relay_name == 'relay3' or relay_name == 'relay4' or relay_name == 'relay5' or relay_name == 'relay6' or relay_name == 'relay7' or relay_name == 'relay8':
			if state == "high":
				high_rele(dic_pins[relay_name],"a")
			elif state == "low":
				low_rele(dic_pins[relay_name],"a")
			else:
				theBody = json.dumps({'412': "Precondition Failed"}) # you seem to want a JSON response
				return HTTPResponse(status=412, body=theBody)
		if relay_name == 'relay9' or relay_name == 'relay10':
			if state == "high":
				high_rele(dic_pins[relay_name],"b")
			elif state == "low":
				low_rele(dic_pins[relay_name],"b")
			else:
				theBody = json.dumps({'412': "Precondition Failed"}) # you seem to want a JSON response
				return HTTPResponse(status=412, body=theBody)
		theBody = json.dumps({'200': relay_name}) # you seem to want a JSON response
		return HTTPResponse(status=200, body=theBody)
	else:
		theBody = json.dumps({'401': 'Unauthorized'}) # you seem to want a JSON response
		return HTTPResponse(status=401, body=theBody)

@route('/relay/status', method='POST')
def estado_dos_reles():
   token = request.forms.get('token')
   valid_token = verify_auth_token(token)
   if valid_token == True:
      theBody = come_back_reles()
      return HTTPResponse(status=200, body=theBody)
   else:
      theBody = json.dumps({'401': 'Unauthorized'}) # you seem to want a JSON response
      return HTTPResponse(status=401, body=theBody)

def come_back_reles():
   aux_str_retorno = ""
   bus.write_byte_data(0x20,0x00,0x00) # Set all of bank A to outputs 
   bus.write_byte_data(0x20,0x01,0x00) # Set all of bank B to outputs
   # Read current values from the IO Expander
   retorno_bank_A =  bus.read_byte_data(address, 0x12)
   #print "{0:b}".format(retorno_bank_A)
   retorno_bank_B =  bus.read_byte_data(address, 0x13)
   #print "{0:b}".format(retorno_bank_B)
   bank_16bits = ( retorno_bank_B << 8) | retorno_bank_A
   #print "{0:b}".format(bank_16bits)

   obj_json = Simple_Json_Object()
   obj_json.relay_status = Simple_Json_Object()
   #obj_json.relay_status.retorno_reles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
   obj_json.status_transistor = Simple_Json_Object()
   #obj_json.status_transistor.retorno_transistor = [0, 0]
   temp_array = []
   #for para montar json de reles
   #for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15]:
   for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
      if (bank_16bits >> n) & 1 :
         temp_array.append(1)
      else:
         temp_array.append(0)
   obj_json.relay_status.return_relays = temp_array
   temp_array = []
   #for n in [10, 11, 12]:
   for n in [11, 10, 12]:
      if (bank_16bits >> n) & 1 :
         temp_array.append(1)
      else:
         temp_array.append(0)
   obj_json.status_transistor.return_transistor = temp_array
   #print(obj_json.to_JSON())
   return obj_json.to_JSON()   

def tooglerelay_func(output, bank):
   # Set the correct register for the banks
   if bank == "a" :
      register = 0x12
   elif bank == "b" :
      register = 0x13
   else:
      print "Error! Bank must be a or b"
   # Read current values from the IO Expander
   value =  bus.read_byte_data(address,register) 
   # Shift the bits for the register value, checking if they are already set first
   if (value >> output) & 1 :
      #already high go to lo low state
      value -= (1 << output)
   else:
      #go to lo high state
      value += (1 << output)
   # Now write to the IO expander
   bus.write_byte_data(address,register,value)

def high_rele(output, bank):
   # Set the correct register for the banks
   if bank == "a" :
      register = 0x12
   elif bank == "b" :
      register = 0x13
   else:
      print "Error! Bank must be a or b"
   # Read current values from the IO Expander
   value =  bus.read_byte_data(address,register) 
   if (value >> output) & 1 :
     print "Output GP"+bank.upper()+str(output), "is already high."
   else:
      value += (1 << output)
   #Now write to the IO expander
   bus.write_byte_data(address,register,value)
   print "\n\r debug high_rele: " + str(value)

def low_rele(output, bank):
   # Set the correct register for the banks
   if bank == "a" :
      register = 0x12
   elif bank == "b" :
      register = 0x13
   else:
      print "Error! Bank must be a or b"
   # Read current values from the IO Expander
   value =  bus.read_byte_data(address,register) 
   if (value >> output) & 1 :
      value -= (1 << output)
   else:
     print "Output GP"+bank.upper()+str(output), "is already low."
   # Now write to the IO expander
   bus.write_byte_data(address,register,value)
   print "\n\r debug low_rele: " + str(value)

run(host='0.0.0.0', port=9000)