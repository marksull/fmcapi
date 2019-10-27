"""Methods to assist making unit_tests"""

import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))
