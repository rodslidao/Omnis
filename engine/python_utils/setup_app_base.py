# from imports import *
import os
import json as js
script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
config_json_dir = script_dir+r'data/json/config'
data_json_dir = script_dir+'data/json/data'
main_dir = script_dir+'..'

class json():
    def __init__(self, _path, create_if_not_exist=False) -> None:
        self.path = _path

        try:
            with open(f"{_path}", 'r', encoding='utf8') as json_file:
                self.json = js.load(json_file)
        except Exception as e:
            print(e)
            self.json = {}
            self.save()
    
    def save(self):
        with open(f"{self.path}", 'w', encoding='utf8') as json_file:
            js.dump(self.json, json_file, ensure_ascii=False, indent=4)

    def get(self, data):
        return self.json.get(data)

    def __call__(self, data=None):
        if isinstance(data, dict):
            self.json = data
        return self.json

    def __str__(self) -> str:
        return str(dict(self.json))

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