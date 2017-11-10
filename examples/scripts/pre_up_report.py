import logging
import os.path
from snactor.loader import load, load_schemas, validate_actor_types, get_actor


_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def show_report(report):
    for key in report:
        print("Errors found on {} modules:".format(key))

        for err in report[key]:
            print("  - {}".format(err))

        print("")


def parse_data(data):
    if 'error' not in data:
        return

    report = {}
    for entry in data['error']:
        if 'value' not in entry or not entry['value']:
            continue

        for err in entry['value']:
            if 'context' not in err or 'value' not in err:
                continue

            report.setdefault(err['context'], []).append(err['value'])

    show_report(report)


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)

    load(os.path.join(_BASE_DIR, 'actors'))
    load_schemas(os.path.join(_BASE_DIR, 'schema'))
    validate_actor_types()

    data = {}
    get_actor('modules_check').execute(data)
    parse_data(data)


if __name__ == '__main__':
    main()
