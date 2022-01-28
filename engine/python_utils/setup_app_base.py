# from imports import *
import os
# import json as js
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
config_json_dir = script_dir+r'data/json/config'
data_json_dir = script_dir+'data/json/data'
main_dir = script_dir+'..'

from common_classes import *

_main_json = json(script_dir+r'\main.json')
_main_copy_json = json(script_dir+r'\config\main_copy.json')
_mainfinal_json = json(script_dir+r'\config\main_final.json')
mainfinal_json = _mainfinal_json()

main_json = _main_json()
main_copy_json = _main_copy_json()

if main_json != main_copy_json:
    print("Config has changed, update base dicts.")
    for jsons in main_json.keys():
        json_file = json(fr"{script_dir}\data\json\config\editable\{jsons}.json")()
        temp = []
        for selected in main_json[jsons]:
            for item in json_file:
                if item == item | selected:
                    temp.append(item)
                    break
        mainfinal_json[jsons] = temp
    _mainfinal_json(mainfinal_json)
    _main_copy_json(main_json)
    _mainfinal_json.save()
    _main_copy_json.save()
else:
    print("Same config, nothing changed")