from asyncio.base_tasks import _task_get_stack
from .models import *

class NavBarElement:
    def __init__(self, tekst, link):
        self.tekst = tekst
        self.link = link
        
class TekstualnoPolje:
    def __init__(self, tekst):
        self.tekst = tekst


class LinkPolje(TekstualnoPolje):
    def __init__(self, tekst, link):
        super().__init__(tekst)
        self.link = link

class SlikaPolje(LinkPolje):
    def __init__(self, tekst, link, slika):
        super().__init__(tekst, link)
        self.slika = slika

class TreningIStavke():
    def __init__(self, trening:Trening, stavke):
        self.trening = trening
        self.stavke = stavke