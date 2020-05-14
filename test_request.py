import argparse

import requests

def main(args):
    with open(args.test_file) as f:
        data = f.read().partition('\n\n')[2]
    response = requests.post("http://localhost:3380/find_related", data=data)
    print(response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_file', required=True)
    args = parser.parse_args()
    main(args)

