from jsl import Document
from jsl.fields import BooleanField, StringField 


class TypePortScan(Document):
    shallow_scan = BooleanField(required=False)
    port_range = StringField(required=False)
    force_nmap = BooleanField(required=False)
