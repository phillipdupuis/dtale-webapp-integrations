import dtale
import numpy as np
import pandas as pd
from django.conf import settings
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect


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


def _table_list_row_html(table_name):
    return f"""
    <tr>
        <td>{table_name}</td>
        <td>
            <a href="/tables/dtale/view/{table_name}/" target="blank" rel="noopener noreferrer">
                <button>View</button>
            </a>
        </td>
        <td>
            <a href="/tables/dtale/refresh/{table_name}/">
                <button>Refresh</button>
            </a>
        </td>
    </tr>
    """


def table_list(request):
    return HttpResponse(
        f"""
    <html>
        <head>
            <title>My Main App</title>
        </head>
        <body>
            <h1>Database Tables</h1>
            <table>
                <tbody>
                    {"".join(_table_list_row_html(name) for name in connection.introspection.table_names())}
                </tbody>
            </table>
        </body>
    </html>
    """
    )


def _get_table_as_dataframe(table_name):
    with connection.cursor() as cursor:
        columns = [
            f.name
            for f in connection.introspection.get_table_description(cursor, table_name)
        ]
        rows = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
        df = pd.DataFrame(rows, columns=columns)
        return df


def view_table_dtale(request, table_name):
    instance = dtale.get_instance(table_name)
    if instance is None:
        df = _get_table_as_dataframe(table_name)
        instance = dtale.app.startup(settings.DTALE_URL, data=df, data_id=table_name)
    return HttpResponseRedirect(instance.main_url())


def refresh_table_dtale(request, table_name):
    instance = dtale.get_instance(table_name)
    if instance is not None:
        df = _get_table_as_dataframe(table_name)
        instance.data = df
    return HttpResponse(status=204)
