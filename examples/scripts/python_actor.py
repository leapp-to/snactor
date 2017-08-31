""" Sample script to test python executor """
from generic_runner import run, pprint, get_actor


def test_python_executor():
    """ Execute osversion actor to test python executor """
    data = {}
    get_actor('osversion').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_python_executor)
