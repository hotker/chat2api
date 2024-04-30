import base64
import hashlib
import json
import random
import time
from datetime import datetime, timedelta, timezone

answers = {}
cores = [8, 12, 16, 24]
screens = [3000, 4000, 6000]
timeLayout = "%a %b %d %Y %H:%M:%S"


def get_parse_time():
    now = datetime.now(timezone(timedelta(hours=-8)))
    return now.strftime(timeLayout) + " GMT-0800 (Pacific Time)"


def get_config(user_agent):
    random.seed(int(time.time() * 1e9))
    core = random.choice(cores)
    screen = random.choice(screens)
    return [core + screen, get_parse_time(), 4294705152, 0, user_agent]


def calc_proof_token(seed, diff, user_agent):
    if seed in answers:
        return answers[seed]

    config = get_config(user_agent)
    diffLen = len(diff) // 2

    for i in range(100000):
        config[3] = i
        json_data = json.dumps(config).encode()
        base = base64.b64encode(json_data).decode()
        hasher = hashlib.sha3_512()
        hasher.update((seed + base).encode())
        hash_value = hasher.digest()

        if hash_value[:diffLen].hex() <= diff:
            result = "gAAAAAB" + base
            answers[seed] = result
            return result

    return "gAAAAABwQ8Lk5FbGpA2NcR9dShT6gYjU7VxZ4D" + base64.b64encode(f'"{seed}"'.encode()).decode()


def chat_requirements_body(user_agent):
    itemlist = get_config(user_agent)
    itemlist += [
        'https://cdn.oaistatic.com/_next/static/2E3kyHMTDQPAokpbyfwns/_ssgManifest.js?dpl=ebab7301ae39fe916a5e1ce6d894b31921d5d573',
        "dpl=ebab7301ae39fe916a5e1ce6d894b31921d5d573",
        "zh-CN",
        "zh-CN, zh"
    ]
    json_data = json.dumps(itemlist).encode()
    base = base64.b64encode(json_data).decode()
    retObj = {'p': 'gAAAAAC' + base}
    return json.dumps(retObj)
