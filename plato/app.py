"""flask app runner"""

import os
from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    """default flask handler"""
    return "Hello, Smarti v0.0.1"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    app.run(debug=True, host="0.0.0.0", port=port)
