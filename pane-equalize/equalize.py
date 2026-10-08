"""Equalize the panes in the current Herdr tab.

A chain of same-direction splits (A | B | C) gets equal shares; a split in the
other direction (B over C) counts as one slot in its parent and is equalized
on its own.
"""
import json
import os
import socket
import sys


def rpc(method, params):
    with socket.socket(socket.AF_UNIX) as s:
        s.connect(os.environ["HERDR_SOCKET_PATH"])
        s.sendall((json.dumps({"id": "equalize", "method": method, "params": params}) + "\n").encode())
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
    reply = json.loads(buf)
    if "error" in reply:
        sys.exit(f"{method}: {reply['error'].get('message', reply['error'])}")
    return reply["result"]


def slots(node, direction):
    """How many equal slots a subtree takes along `direction`."""
    if node["type"] == "split" and node["direction"] == direction:
        return slots(node["first"], direction) + slots(node["second"], direction)
    return 1


def ratios(node, path=()):
    """Yield (path, ratio) for every split; path is root-to-split, True = second child."""
    if node["type"] != "split":
        return
    first = slots(node["first"], node["direction"])
    second = slots(node["second"], node["direction"])
    yield list(path), first / (first + second)
    yield from ratios(node["first"], path + (False,))
    yield from ratios(node["second"], path + (True,))


def main():
    target = {"tab_id": os.environ["HERDR_TAB_ID"]} if os.environ.get("HERDR_TAB_ID") else {}
    layout = rpc("layout.export", target)["layout"]
    for path, ratio in ratios(layout["root"]):
        rpc("layout.set_split_ratio", {"tab_id": layout["tab_id"], "path": path, "ratio": ratio})


if __name__ == "__main__":
    main()
