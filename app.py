import json
import zmq
from datetime import datetime

MIN_ACCURACY = 0.9

# Simple search helpers


# returns an accuracy metric (how close the lengths are of two strings that presumably start with the same chars)
def check_accuracy(shorter, longer, min_accuracy):
    shorter_len = len(shorter)
    longer_len = max(len(longer), 1)
    return shorter_len / longer_len >= min_accuracy


def search_partial(collection, partial, min_accuracy):
    search = partial.lower().strip()
    results = [
        item
        for item in collection
        if (
            item.get("name", "").lower().strip().startswith(search)
            and check_accuracy(
                search, item.get("name", "").lower().strip(), min_accuracy
            )
        )
    ]
    return results


def search_alias(collection, query):
    query = query.lower().strip()
    for item in collection:
        primary = item.get("name", "").lower()
        aliases = [a.lower().strip() for a in item.get("aliases", [])]
        if query == primary or query in aliases:
            return item
    return None


def call(collection, sort_by, target_value):
    if sort_by == "partial_name":
        return search_partial(collection, target_value, MIN_ACCURACY)
    elif sort_by == "alias":
        return search_alias(collection, target_value)
    elif sort_by == "all":
        return search_alias(collection, target_value) + search_partial(
            collection, target_value, MIN_ACCURACY
        )
    else:
        return []


def server():
    print("Starting server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5016")

    while True:
        print("Listening for requests...")
        message = socket.recv()
        full_msg = message.decode()

        if full_msg == "Q":
            print("Received terminate message. Stopping program.")
            break

        json_data = json.loads(full_msg)
        collection = json_data.get("collection", [])
        sort_by = json_data.get("sort_by", "")
        target_value = json_data.get("target_value", "")

        print(f"Received request:\n   sort_by: {sort_by}, target_value: {target_value}")
        result = call(collection, sort_by, target_value)
        socket.send_string(json.dumps({"result": result}))

    context.destroy()
    socket.close()


if __name__ == "__main__":
    server()
