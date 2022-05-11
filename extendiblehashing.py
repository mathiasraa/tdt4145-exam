BUCKET_SIZE = 3
INPUT = [
    4068,
    1752,
    3429,
    2130,
    2854,
    1591,
    2203,
    1423,
    3017,
    2333,
    3923,
    4817,
    4876,
    1428,
]

# INPUT = [16, 4, 6, 22, 24, 10, 31, 7, 9, 20, 26]
INITIAL_DEPTH = 2
INITIAL_SIZE = 2**INITIAL_DEPTH
HASH_MODULO = 16


def HASH_FUNCTION(k):
    return "{0:04b}".format(k % HASH_MODULO)


class Block:
    def __init__(self, depth=INITIAL_DEPTH):
        self.depth = depth
        self.values = []
        self.connected = None

    def __str__(self) -> str:
        return str(self.values)


class Catalog:
    def __init__(self, depth=INITIAL_DEPTH):
        self.depth = depth
        self.blocks = {
            "{0:0{depth}b}".format(i, depth=self.depth): Block(depth=self.depth)
            for i in range(0, INITIAL_SIZE)
        }

    def __str__(self) -> str:
        result = "\nglobal depth: " + str(self.depth) + "\n"

        for key, value in self.blocks.items():
            if value.connected:
                result += key + " -> " + str("0" + key[1:]) + "\n"
            else:
                result += (
                    key
                    + " -> "
                    + str(value)
                    + " local depth: "
                    + str(value.depth)
                    + "\n"
                )

        return result

    def size(self):
        return len(self.blocks.keys())

    def insert(self, value):
        key = HASH_FUNCTION(value)[-self.depth :]
        block = self.blocks[key]
        length = len(block.values)

        if (
            not block.connected or len(block.connected.values) < BUCKET_SIZE
        ) and length < BUCKET_SIZE:

            if block.connected:
                block = block.connected

            if len(block.values) == 0 and block.depth <= self.depth - 1:
                block.depth += 1
            block.values.append(value)

        elif block.depth < self.depth:

            if block.connected:
                key = "0" + key[1:]

            new_values = self.blocks[key].values + [value]

            self.blocks[key] = Block(depth=self.depth)
            self.blocks[key].connected = None
            self.blocks["1" + key[1:]].connected = None

            for val in new_values:
                self.insert(val)
        else:
            new_values = self.blocks[key].values + [value]

            self.depth += 1
            self.blocks[key] = Block(depth=self.depth)

            extension = range(self.size(), self.size() * 2)
            self.blocks = {"0" + key: value for key, value in self.blocks.items()}

            for i in extension:
                self.blocks["{0:0{depth}b}".format(i, depth=self.depth)] = Block(
                    depth=self.depth - 1
                )

            for val in new_values:
                self.insert(val)

            for key, block in self.blocks.items():
                if len(block.values) == 0:
                    block.connected = self.blocks["0" + key[1:]]
                else:
                    block.connected = None


catalog = Catalog()

for value in INPUT:
    catalog.insert(value)
    print(catalog)
