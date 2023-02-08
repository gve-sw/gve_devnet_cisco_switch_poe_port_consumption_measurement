# Measuring power consumption on PoE ports for Cisco Switches

This project is about creating a automated way to measure and store the power consumption used by PoE ports in a switch environment.
The solution is a python script that extracts, transforms and load the data into an InfluxDB database.

## Getting Started

You will need to install python and two libraries for this solution to work. This is further described below. Furthermore, configuring energywies on the source switches is necessary for the data source to be activated. 

### Prerequisites

Download Python 3.x.y: https://www.python.org/downloads/windows/

Pip should be included in Python installation, if not, download Pip too.
Download Pip: https://pip.pypa.io/en/stable/installing/

```
Download and install Python 3.
```

Guide to configure Energywise: https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst_digital_building_series_switches/software/15-2_7_e/b_1527e_consolidated_cdb_cg/configuring_energywise.html

Device credentials must be added to devices.json (further described below)

The solution use InfluxDB as storage. This must be set up separately. 
- Guide on setting up InfluxDB can be found here: https://docs.influxdata.com/platform/install-and-deploy/deploying/sandbox-install
- Guide for Windows deployments: https://devconnected.com/how-to-install-influxdb-on-windows-in-2019/
- Database instance credentials must be inserted into series_helper.py

### Installing

Install project requirements:

```
pip install -r requirements.txt
```

## Running the program

Ensure that you have Layer 3 connectivity to the switches from the device you will be running the program on. Switch credentials have to be inserted into the devices.json as well as switches must be configured with an energywise domain. Make sure series_helper.py have the database credentials for your environment. 

Execute program with the following command
```
python main.py
```


## Running the tests

This project is simply a proof of concept are do not have any automated tests.

## License
Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE)

## Code of Conduct
Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing
See our contributing guidelines [here](./CONTRIBUTING.md)

## Built With

* [Netmiko] (https://pynet.twb-tech.com/blog/automation/netmiko.html) - To connect through SSH to remote switches
* [InfluxDB] (https://docs.influxdata.com/influxdb/v1.7/tools/api/) - Database API

## Versioning
This project uses python3.7, as well as libraries influxdb version 5.2.3 and netmiko version 3.0.0.
See section 'Installing' to install project dependencies.

## Authors

* **Kristian Langvann** 
* **Josef Kandelan** 

## Files & Functions

### devices.json

devices.json contains the devices (switches) that you want to monitor automatically. Every device in 
this file will be part of the power consumption measurements. Devices are added in the following json format:

```

  "[Device Name]": {
    "device_type": "[Device Type]",
    "host": "[Host IP]",
    "username": "[Username]",
    "password": "[Password]"
  } 

```

* Device Name - Arbitrary device name
* Device Type - Netmiko device type, supported device types can be found here: https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py#L70 ('cisco_ios' is default for Cisco devices)
* Username - SSH username
* Password - SSH Password

Example:

```

  "mSwitch": {

  }
  
```

### main.py

main.py contains the main logic of the script. Each function will be described in detail below in the order they should be used.

#### get_device_details(filename) 

This function extract the information stored in 'filename' and returns a list containing multiple dictionaries. 

* Input: filename - The name of the file where you store your devices, in our case 'devices.json'
* Output: login - A list of dictionaries (one for each device) including the information stored in devices.json for that device

It is important that your file is in the same folder as your script in order to put in the filename as a string alone. Otherwise, you need to input the 
entire path of your file. 


Example:

```

get_device_details('devices.json')

or 

get_device_details('C:\Users\myUser\myProjectFolder\devices.json')

```

#### initialize_ssh(login)

This function connects through SSH to the remote switches. 

* Input: Need SSH login credentials, ip and device_type from devices.json to establish connectiong. Every dict returned from get_device_details can be used as input.
* Output: The SSH session object of the switch that you are currently connected to

Example: 

```

initialize_ssh('login')

```

#### get_switch_power_total_interfaces(ssh_connection)

This function queries each switch for the PoE consumption on each port and writes this information to the InfluxDB database. 

Input: ssh_connection - The SSH session object of the switch that you are currently connected to. 

The function does not return anything but writes the following query: 'energywise query importance 100 name * collect usage' in the switch in Priveliged Exec mode.
The switched output is parsed to contain only Host IP, Interface Name, Power Consumption, Metric, Level & Importance as individual values. 

* Host IP - The IP-address of the currently connected switch
* Interface Name - The name of the interface that is currently being monitored
* Power Consumption - The PoE consumption of the currently monitored interface  
* Metric - The metric used to represent PoE consumption
* Level - The Energywise power levels that range from 0-10 where 10 is full power consumption and the default value
* Importance - The rating of your devices based on the business or deployment context that range between 0-100, 1 being least important and the default value

Example:

```

get_switch_power_total_interfaces('initialize_ssh(login)')


```











   



 
