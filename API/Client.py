from suds.client import Client
from suds.cache import NoCache
import logging
from dicttoxml import dicttoxml

# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
client = Client('http://127.0.0.1:8000/soap/?WSDL', cache=NoCache())


re = client.service.get_services()
print(re)