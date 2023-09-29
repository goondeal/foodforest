import json
from django.core.management.base import BaseCommand
from management.models import *


class Command(BaseCommand):
    help = 'Adds country data to the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to <file>.json')

    def _is_english(self, text):
        return text.encode().isalpha()

    def handle(self, *args, **kwargs):
        fpath = kwargs['file_path']
        data = None
        with open(file=fpath, mode='r', encoding='utf-8') as f:
            data = json.loads(f.read())
        
        country = Country.objects.create(name=data['name'], name_ar=data['name_ar'])
        states = data["states"]
        for i in range(len(states)):
            s = states[i]
            state = State.objects.create(
                name=s["name"],
                name_ar=s["name_ar"],
                country=country,
                ordering=i
            )
            for j in range(len(s["cities"])):
                c = s["cities"][j]
                city = City.objects.create(
                    name=c["name"],
                    name_ar=c["name_ar"],
                    state=state,
                    ordering=j
                )
