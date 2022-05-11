import math

import pandas as pd

numbers = [10, 11, 12, 13, 14, 15, 16, 17, 18]
modulo = 4


def hash_func(k):
    return "{0:0{length}b}".format(k % modulo, length=int(math.sqrt(modulo)))


def main():
    result = [hash_func(num) for num in numbers]
    data = {"Numbers": numbers, "Hashed": result}

    df = pd.DataFrame(data)

    print("-" * 20 + "\n")
    print(df)
    print("\n" + "-" * 20)


if __name__ == "__main__":
    main()
