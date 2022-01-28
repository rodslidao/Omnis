from I_class import *
def fabric(output, main_config_model, cameras_objects, machine_objects, filters_json):
    identificator_objects = {}
    for key, config in main_config_model.items():
        identificator_objects[config.get('filter')] = identificador(
            name=config.get('filter'),
            cam=cameras_objects.get(config.get('camera_device')),
            machine=machine_objects.get(config.get('machine')),
            filter_data=filters_json.value
            )