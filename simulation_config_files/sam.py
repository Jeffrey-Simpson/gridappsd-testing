# name = {'ln1047pvfrm_sw':0, 'ln0895780_sw':1,  'ln5001chp_sw':2}
# for switch in response["data"]:
#     equipment_dict[switch["id"]] = switch
#     if switch['IdentifiedObject.name'] in {'ln1047pvfrm_sw','ln0895780_sw','ln5001chp_sw'}: 
#     	switch_mrid1[name[switch['IdentifiedObject.name']]] = switch['IdentifiedObject.mRID']
#     	switch_mrid2[name[switch['IdentifiedObject.name']]] = switch['IdentifiedObject.mRID']

import json 

with open("simulation_config_files/9500-alarm-config.json", "r") as file:
	run_config = json.load(file)

events = run_config["test_config"]["events"]
print(events)
switch_mrid1 = [ events[i]["message"]["forward_differences"][0]["object"] for i in range(len(events))]
print(switch_mrid1)