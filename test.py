import zmq
import json
import time

SOCKET_ADDR = "tcp://localhost:5016"

TERMINATE_APP = False

SAMPLE_COLLECTION = [
    {"name": "APT.", "aliases": [], "date": "10-01-2025"},
    {"name": "It Will Rain", "aliases": [], "date": "10-12-2025"},
    {
        "name": "Nothin' On You",
        "aliases": ["Nothing On You", "Nothin On You"],
        "date": "10-12-2025",
    },
]

SAMPLE_CALL_1 = {
    "collection": SAMPLE_COLLECTION,
    "sort_by": "partial_name",
    "target_value": "It Will Rain",
}

SAMPLE_CALL_2 = {
    "collection": SAMPLE_COLLECTION,
    "sort_by": "alias",
    "target_value": "Nothing On You",
}


def runClient(call):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(SOCKET_ADDR)

    sample_json = json.dumps(call)

    socket.send_string(sample_json)

    response = socket.recv()
    data = json.loads(response.decode())

    print(f"Microservice returned: {data}")

    if TERMINATE_APP:
        print("Terminating app program.")
        socket.send_string("Q")

    context.destroy()


if __name__ == "__main__":
    TERMINATE_APP = False
    runClient(SAMPLE_CALL_1)
    TERMINATE_APP = True
    runClient(SAMPLE_CALL_2)
