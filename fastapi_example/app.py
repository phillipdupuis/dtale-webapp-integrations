import dtale
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

HOST = "localhost"
PORT = 5000
DTALE_HOST = "dtale.localhost"
DTALE_URL = f"http://{DTALE_HOST}:{PORT}"

main_app = FastAPI()

dtale.app.initialize_process_props(DTALE_HOST, PORT, False)
dtale_app = WSGIMiddleware(dtale.app.build_app(DTALE_URL, host=DTALE_HOST))


@main_app.get("/", response_class=HTMLResponse)
async def root():
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


@main_app.get("/dtale/{data_id}/")
async def show_dtale(data_id):
    instance = dtale.get_instance(data_id)
    if instance is None:
        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=list("ABC"))
        instance = dtale.app.startup(DTALE_URL, data=df, data_id=data_id)
    return RedirectResponse(instance.main_url())


async def combined_app(scope, receive, send):
    """
    Dispatch requests to the appropriate app based on the subdomain
    """
    for header in scope.get("headers", []):
        name, value = [x.decode() for x in header]
        if name == "host":
            host = value.split(":")[0]
            if host == DTALE_HOST:
                return await dtale_app(scope, receive, send)
            break

    return await main_app(scope, receive, send)


if __name__ == "__main__":
    uvicorn.run(combined_app, host=HOST, port=PORT, debug=True)
