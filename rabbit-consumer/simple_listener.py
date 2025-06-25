import subprocess
import json
from urllib.parse import urlparse
from os import path

"""
Make sure you are running this in rabbitmq pod with correct transporturl
"""

# set oslo messaging transport-url from nova-confs
TRANSPORT_URL = ""

# As of now Nova suports both versioned and unversioned(notifications.info) notifications
QUEUES = ["versioned_notifications.info", "notifications.info"]
PROCESS_QUEUE = QUEUES[0]

# basic check for first time run
if TRANSPORT_URL == "":
    print("XXX - ERR - set oslo messaging transport-url from nova-confs")
    print("Make sure to verify which queue you are listening to, by-default its versioned.")
    print("\nTip: Run with watch - ex: watch python3 code.py")
    exit(1)

def get_data(queue, transport_url):
    tp = urlparse(transport_url)
    if not path.exists("/tmp/rabbitmqadmin"):
        # download rabbitadmin using curl cmd in same pod
        # curl http://localhost:15672/cli/rabbitmqadmin > /tmp/rabbitmqadmin
        subprocess.getoutput("curl http://localhost:15672/cli/rabbitmqadmin > /tmp/rabbitmqadmin")
        subprocess.getoutput("chmod +x /tmp/rabbitmqadmin")

    cmd = f'/tmp/rabbitmqadmin -u {tp.username} -p {tp.password} -V / -H localhost -P 15672   get queue={queue}  count=-1 --format=raw_json'

    return json.loads(subprocess.getoutput(cmd))

def show_unversioned_notifications(msg):
    event = instance = publisher_host = state = None

    try:
        event = msg.get('event_type', None)
        instance = msg['payload'].get('instance_id', None)
        if instance:
            instance += f"- ({msg['payload'].get('display_name')})"
        publisher_host = msg.get('publisher_id', None)
        state = msg['payload'].get('state', None)
        host = "None"
        time_s = "#ToDo"

        return (instance, host,  publisher_host, event, state, time_s)

    except Exception as ex:
        # print("ex:", ex, end="\n")
        pass


def show_versioned_notifications(msg):
    event = instance = publisher_host = t_state = state = None
    host = None
    try:

        event = msg.get('event_type', None)
        publisher_host = msg.get('publisher_id', None)
        time_s = msg['timestamp'].split()[1]

        nova_obj = msg['payload']['nova_object.data']
        instance = nova_obj.get('uuid', None)
        if instance:
            instance += f"- ({nova_obj.get('display_name')})"
        
        t_state = nova_obj.get('task_state', None)
        state = nova_obj.get('state', None)
        host = nova_obj.get('node', None)
        
        return [str(e) for e in [instance, host, publisher_host, event, t_state, state, time_s]]
    except Exception as ex:
        # print("ex:", ex, end="\n")
        pass

def main():
    try:
        data = get_data(PROCESS_QUEUE, TRANSPORT_URL)
    except Exception as ex:
        print("rabbitmq admin cmd ex:", ex, end="\n")
        exit(1)
    pr_req_id = ""
    for each in data[-15:]:
        payload = json.loads(each['payload'])
        msg = json.loads(payload['oslo.message'])

        if each['routing_key'] == "versioned_notifications.info":
            s, h, p_h, e, t_st, st, time_s = show_versioned_notifications(msg)

        else:
            s, h, p_h, e, st, tmie_s = show_unversioned_notifications(msg)
            # unversioned do not have task_state
            t_st = "---"

        if msg['_context_request_id'] != pr_req_id:
            pr_req_id = msg['_context_request_id']
            print(f"\n{pr_req_id}, {s}")
        print(f"    {time_s}   {h:<40}\t{str(p_h):<35}\t{e:<30}\t{t_st:<20}\t{st}")
main()
