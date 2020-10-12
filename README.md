# Dtale web app examples
Code examples illustrating how dtale can be safely integrated into existing python web applications.

Currently this requires that the dtale app(s) use a subdomain, such as "dtale.example.com" instead of "example.com"; you can then wrap your existing WSGI/ASGI application in a dispatch WSGI/ASGI application which will check the host name for each request to decide if it should be handled by the main app or dtale app.

## Local development

To test utilizing subdomains locally, you will need to update your `/etc/hosts` file.

If you're on mac/linux, from a terminal:
1. `sudo vi /etc/hosts`
2. make sure that entries exist mapping both "localhost" and "dtale.localhost" to 127.0.0.1:
```
127.0.0.1    localhost
127.0.0.1    dtale.localhost
```

Then, look at the example for your particular framework.

Will update this with framework-specific advice in the near future...

