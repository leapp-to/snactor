""" Sample script to test output processors """
from generic_runner import run, pprint, get_actor


def test_output_processors():
    """ Execute iplist actor to test output processors """
    data = {}
    print("Before execution")
    print("=" * 70)
    pprint(data)
    print("=" * 70)
    print("Execution result:",
          get_actor('iplist').execute(data))
    print("=" * 70)
    print("After execution")
    pprint(data)


if __name__ == '__main__':
    run(test_output_processors)
