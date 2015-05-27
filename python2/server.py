"""Python web server.

Requires Flask. Install with:

    pip install Flask

or:

    pip install -r requirements.txt

"""

import datetime
import flask
import json
import uuid

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def get_it():
    data = {
        "UTCDatetime": utcnow().isoformat(),
        "UUID": str(uuid.uuid4()),
    }
    return flask.jsonify(data)


@app.route('/uuid/<the_uuid>', methods=['POST'])
def post_it(the_uuid):
    try:
        the_uuid = uuid.UUID(the_uuid)
    except ValueError as ex:
        return 400, ex.message  # Yep, this isn't the best thing to return...
    data = {
        "UTCDatetime": utcnow().isoformat(),
        "UUID": str(the_uuid),
    }
    return flask.jsonify(data)


def utcnow():
    return datetime.datetime.utcnow().replace(microsecond=0)


if __name__ == '__main__':
    app.run()
