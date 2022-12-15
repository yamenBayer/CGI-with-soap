class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield 'Hello, %s' % name
application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=XmlDocument()
)
# This module resides in a package in your Django
# project.
hello_app = csrf_exempt(DjangoApplication(application))
# hello_app here has to be put in a package that is
# listed in the INSTALLED_APPS list in your settings.py
# and referenced in the url.py under an appropriate
# regexp entry.