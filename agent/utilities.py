import zlib
import json
import uuid
from base64 import b64encode

def zip_struct(data):
    return zlib.compress(json.dumps(data).encode('utf-8'))

## json_scheme
#     agent_id
#     zip_report_json
def gen_report_zip(agent_id, report_dict):
    json_report_zipped = {
        "agent_id": agent_id,
        "zip_report": b64encode(zip_struct(report_dict)).decode()
    }

    return json_report_zipped


def generate_agent_id():
    return str(uuid.uuid4())
