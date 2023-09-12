import monkey
import yaml


cippo = None

# this is called at the very beginning,
# before loading 1st room. Here we initialize all object maps
def on_startup():
    global cippo
    with open("assets/objects.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for key, value in data['objects'].items():
                room = value['room']
                cippo.objects[key] = value
                if room not in cippo.objects_in_room:
                    cippo.objects_in_room[room] = []
                cippo.objects_in_room[room].append(key)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    if not hasattr(cippo, "string_file"):
        print('required: string_file')
        exit(1)

    with open("assets/" + cippo.string_file, "r") as stream:
        try:
            cippo.strings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
def sima(c):
    global cippo
    cippo = c


def ciano():
    global cippo
    print(cippo.room_id)
    print('sela')
    cippo.on_startup = on_startup


