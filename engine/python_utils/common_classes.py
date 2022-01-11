import json as js
class json():
    def __init__(self, _path, create_if_not_exist=False) -> None:
        self.path = _path

        try:
            with open(f"{_path}", 'r', encoding='utf8') as json_file:
                self.json = js.load(json_file)
        except Exception as e:
            self.json = {}
            if create_if_not_exist:
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