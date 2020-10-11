import dtale
import numpy as np
import pandas as pd
from flask import Flask, redirect

HOST = "pdupuis.com"
PORT = 5000
DTALE_HOST = "dtale.pdupuis.com"
DTALE_URL = f"http://{DTALE_HOST}:{PORT}"

main_app = Flask(__name__)

dtale.app.initialize_process_props(DTALE_HOST, PORT, False)
dtale_app = dtale.app.build_app(DTALE_URL, host=DTALE_HOST)


class CombinedWsgiApp:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        host = environ.get("HTTP_HOST", "").split(":")[0]
        if host == DTALE_HOST:
            return dtale_app(environ, start_response)
        return self.wsgi_app(environ, start_response)


main_app.wsgi_app = CombinedWsgiApp(main_app.wsgi_app)


@main_app.route("/")
def root():
    return """
    <html>
        <head>
            <title>My Main App</title>
        </head>
        <body>
            <h1>D-Tale Instances</h1>
            <a href="/dtale/example-one/" target="_blank" rel="noopener noreferrer">D-Tale Instance #1</a><br/>
            <a href="/dtale/example-two/" target="_blank" rel="noopener noreferrer">D-Tale Instance #2</a><br/>
        </body>
    </html>
    """


@main_app.route("/dtale/<data_id>/")
def show_dtale(data_id):
    instance = dtale.get_instance(data_id)
    if instance is None:
        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=list("ABC"))
        instance = dtale.app.startup(DTALE_URL, data=df, data_id=data_id)
    return redirect(instance.main_url())


if __name__ == "__main__":
    main_app.run(host=HOST, port=PORT, debug=True)
