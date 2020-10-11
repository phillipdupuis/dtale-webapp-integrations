from django.http import HttpResponse, HttpResponseRedirect
import dtale
import pandas as pd
import numpy as np
from django.conf import settings


def root(request):
    return HttpResponse(
        """
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
    )


def show_dtale(request, data_id):
    instance = dtale.get_instance(data_id)
    if instance is None:
        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=list("ABC"))
        instance = dtale.app.startup(settings.DTALE_URL, data=df, data_id=data_id)
    return HttpResponseRedirect(instance.main_url())
