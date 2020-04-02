import random
import string


def gen_random_str(length: int = 12) -> str:
    return "".join([random.choice(string.ascii_letters) for i in range(length)])
