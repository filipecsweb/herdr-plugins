from equalize import ratios


def pane():
    return {"type": "pane"}


def split(direction, first, second):
    return {"type": "split", "direction": direction, "ratio": 0.5, "first": first, "second": second}


# A | (B | (C over D)): three equal columns, C and D equal height.
tree = split("right", pane(), split("right", pane(), split("down", pane(), pane())))
assert list(ratios(tree)) == [([], 1 / 3), ([True], 1 / 2), ([True, True], 1 / 2)]

# (A | B) | C, nested on the left this time.
tree = split("right", split("right", pane(), pane()), pane())
assert list(ratios(tree)) == [([], 2 / 3), ([False], 1 / 2)]

assert list(ratios(pane())) == []
print("ok")
