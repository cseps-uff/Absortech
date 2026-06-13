import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAbsortech.settings')
django.setup()

from app.views import obter_leituras
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/api/leituras/')

try:
    response = obter_leituras(request)
    print('Status:', response.status_code)

    if hasattr(response, 'data'):
        print('Data:', response.data)
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
