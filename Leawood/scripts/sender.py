
import os
import sys
import django
import channels.layers


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Leawood_XA.settings")
cwd = os.getcwd()
sys.path.append(cwd)

django.setup()

channel_layer = channels.layers.get_channel_layer()
from asgiref.sync import async_to_sync
async_to_sync(channel_layer.send)('test_channel', {'type': 'test.print', 'text':'a message from afar'})

