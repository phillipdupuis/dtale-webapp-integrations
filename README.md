# Dtale web app examples
Code examples illustrating how dtale can be safely integrated into existing python web applications.

Currently this requires that the dtale app(s) use a subdomain, such as "dtale.example.com" instead of "example.com"; you can then wrap your existing WSGI/ASGI application in a dispatch WSGI/ASGI application which will check the host name for each request to decide if it should be handled by the main app or dtale app.

## Local development

To test utilizing subdomains locally, you will need to update your `/etc/hosts` file.

If you're on mac/linux, from a terminal:
1. `sudo vi /etc/hosts`
2. add an entry that ends with .com -- you will use this as your host for testing from now on, rather than localhost or 127.0.0.1.
3. add an entry that matches the previous one but also has "dtale" subdomain prefix.

Example:
```
127.0.0.1    pdupuis.com
127.0.0.1    dtale.pdupuis.com
```

Then, look at the example for your particular framework.

Will update this with framework-specific advice in the near future...

