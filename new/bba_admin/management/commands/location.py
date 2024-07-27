from django.core.management.base import BaseCommand
import json
from bba_admin.models import State, City, Country

class Command(BaseCommand):
    def handle(*args, **kwargs):
        with open('location.json', 'r') as f:
            data = json.load(f)
            
            state = list(data.keys())
        
        country_obj = Country.objects.filter(id=1).first()
        for i in state:
            state = State.objects.create(name=i, country=country_obj)

        for key, value in data.items():
            state_obj = State.objects.filter(name=key).first()
            
            for i in value:
                city = City.objects.create(state=state_obj, name=i)




