from uuid import uuid4


def generate_and_print_sixteen_uuids():
    for _ in range(16):
        print(uuid4())


generate_and_print_sixteen_uuids()
