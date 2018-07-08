import os
import json


def dump_output(data, filename="", dir=""):
    """
    :param data:
    :param filename:
    :param dir:
    :return:
    """
    if not filename:
        return False

    # Check for directory existence
    filename = os.path.join(os.path.curdir, 'output', 'data', filename)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'w') as output_file:
        output_file.write(json.dumps(data,
                                     sort_keys=True,
                                     indent=4))


def load_output(filename, dir=""):
    if not filename:
        return False

    filename = os.path.join(os.path.curdir, 'output', 'data', filename)

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
