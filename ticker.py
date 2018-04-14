import threading
import json


class DataManager:
    def update(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def write(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a] = b
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def list_update(filename, a, b):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        data[a].append(b)
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def delete(filename, a):
        with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
        del data[str(a)]
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)

    def read(filename):
        with open(filename) as f:
            stuff = json.load(f)
        return stuff


def f(f_stop):
    a = DataManager.read('data/activity.json')['timeleft']
    a = int(a)
    b = DataManager.read('data/xp.json')
    e = {}
    if a == 0:
        x = DataManager.read('data/xp.json')
        organized = sorted(x, key=x.get, reverse=True)
        c = 0
        for d in organized:  # Forloop to cache xp.json
            c += 1
            if not c >= 4:
                e[d] = DataManager.read('data/xp.json')[str(d)]
            else:
                break

        for k in b:   # forloop to empty xp.json
            DataManager.delete('data/xp.json', k)

        DataManager.write('data/activity.json', 'last-week', e)
        print("set to e")
        DataManager.write('data/activity.json', 'done', True)
    else:
        DataManager.delete('data/activity.json', 'timeleft')
        DataManager.write('data/activity.json', 'timeleft', a - 60)
        print("")
    if not f_stop.is_set():
        threading.Timer(60, f, [f_stop]).start()


f_stop = threading.Event()
f(f_stop)
