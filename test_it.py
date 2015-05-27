"""Verify a server instance.

This requires python requests.
"""

import click
import datetime
import json
import logging
import requests
import sys
import uuid


@click.command()
@click.option('--verbose/--no-verbose', default=False, help='Enable verbose output.')
@click.option('--base-url', default='http://localhost:5000/', show_default=True)
def main(verbose, base_url):
    _setup_logging(verbose)
    t = Tester(base_url)
    t.test_get()
    t.test_post()
    t.test_bad_post()
    print('SUCCESS!')


class Tester(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def test_get(self):
        url = self.base_url
        resp = requests.get(url)
        resp.raise_for_status()
        self.check_resp(resp)

    def test_post(self):
        uuids = [
            uuid.UUID('00000000-0000-0000-0000-000000000000'),
            uuid.UUID('{deadbeef-dead-beef-dead-beefdeadbeef}'),
            uuid.uuid4(),
            uuid.uuid4(),
        ]
        bu = self.base_url

        for u in uuids:
            url = '{}uuid/{}'.format(bu, u)
            resp = requests.post(url, data='')
            resp.raise_for_status()
            self.check_resp(resp)

            actual_uuid = uuid.UUID(resp.json()['uuid'])
            assert actual_uuid == u, 'POST request returned unexpected UUID. Got: {} Expected: {}'.format(actual_uuid, u)

    def test_bad_post(self):
        url = '{}uuid/bad_uuid'.format(self.base_url)
        resp = requests.post(url, data='')
        assert resp.status_code != 200

    def check_resp(self, resp):
        assert 'application/json' == resp.headers['content-type'], 'incorrect content-type header'

        data = resp.json()
        assert 'utc_datetime' in data.keys(), 'utc_datetime key missing from response'
        assert 'uuid' in data.keys(), 'uuid key missing from response'

        try:
            dt = datetime.datetime.strptime(data['utc_datetime'], '%Y-%m-%dT%H:%M:%S')
        except ValueError as ex:
            print('Failed to parse UTC datetime value: {}'.format(data['utc_datetime']))
            sys.exit(1)

        try:
            u = uuid.UUID(data['uuid'])
        except ValueError as ex:
            print('Failed to parser UUID value: {}'.format(data['uuid']))
            sys.exit(1)


def _setup_logging(verbose):
    log_level = logging.WARN if not verbose else logging.DEBUG
    logging.basicConfig(level=log_level, format='%(levelname)s [%(module)s] %(msg)s')
    logging.debug('Verbose output enabled.')


if __name__ == '__main__':
    main()
