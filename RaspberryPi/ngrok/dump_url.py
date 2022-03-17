import json
from os import popen
from time import sleep
import signal

STOPPEED = False

def dump_url(host='localhost', port='4040'):
    try:
        url = sorted([
            dict(
                zip(
                    ('proto', 'url', 'port'),
                    filter(
                        None,
                        (
                            x.split(':')[0],
                            x.split(':')[1],
                            str(x.split(':')[-1]) if len(x.split(':')[-1]) <= 10 else None
                        )
                    )
                )
            ) for x in (
                popen(f'curl -s {host}:{port}/api/tunnels | jq ".tunnels[].public_url"').read()
            ).replace('\n', '').replace('://', ':').replace('""', '|').replace('"', '').split('|')
        ], key=lambda x: len(x['proto']))
    except IndexError:
        url = [{'proto': 'off-line', 'url': 'off-line', 'port': 'off-line'}]
    return url

def stop(sig, frame):
    global STOPPEED
    STOPPEED = True

signal.signal(signal.SIGTERM, stop)

default = None
while not STOPPEED:
    new = dump_url()
    if new != default:
        default = new
        with open('.url_host', 'w') as outfile:
            json.dump(new, outfile)

    sleep(2)