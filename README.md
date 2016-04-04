# Raspberry_exp_board
This project provides REST, JSON, interface to relays, digital and analog inputs. using simple bottle python web framework.

It also uses some other python libraries that are not installed on Raspbian by default:
* Bottle
* raspberry-gpio-python

# Installing dependences

sudo apt-get install python-rpi.gpio python3-rpi.gpio

sudo apt-get install python-pip

sudo pip install bottle

sudo apt-get install python-smbus

sudo apt-get install python-dev

# Running application
sudo python api_digital_inputs.py

sudo python api_relay.py


#Examples request set high Transistor


api_relay.py

    curl -X POST -F "token=2e52d3eb834e09f30509fcf4837478f207e71f59" -F "transistorname=transistor2" -F "state=low" "http://192.168.0.103:9000/relay/transistor_on_off"

Possibilities:

    transistorname = transistor1 ... transistor3
    state= low or high

Example return:

    {"200": "transistor2"}


#Example request toogle relay
api_relay.py

    curl -X POST -F "token=2e52d3eb834e09f30509fcf4837478f207e71f59" -F "relayname=relay1" "http://192.168.0.103:9000/relay/toogle_relay"

Possibilities:

    relayname = relay1 ... relay10

Return Example:

    {"200": "relay1"}


#Example request set relay high
api_relay.py

    curl -X POST -F "token=2e52d3eb834e09f30509fcf4837478f207e71f59" -F "relayname=relay10" -F "state=high"     "http://192.168.0.103:9000/relay/on_off"

Possibilities:

    relayname = relay1 ... relay10
    state= low or high

Example return:

     {"200": "relay10"}


# Exemple request retur relay status:
api_relay.py

    curl -X POST -F "token=2e52d3eb834e09f30509fcf4837478f207e71f59" "http://192.168.0.103:9000/relay/status"

Example return:

       {
           "relay_status": {
               "return_relays": [
                   0, 
                   0, 
                   0, 
                   0, 
                   0, 
                   0, 
                   0, 
                   0, 
                   0, 
                   1
               ]
           }, 
           "status_transistor": {
               "return_transistor": [
                   1, 
                   0, 
                   1
               ]
           }
       }


# Example request read all digital inputs:
api_digital_inputs.py

    curl -X POST  -F "token=2e52d3eb834e09f30509fcf4837478f207e71f59" "http://192.168.0.103:9001/input/state"

Example return:

    {
    "inputs": {
        "input_state": [
            0, 
            0, 
            0, 
            0, 
            0, 
            1, 
            0, 
            0
        ]
    }
    }
