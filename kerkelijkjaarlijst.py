__author__ = 'sybrandb'
from feestdag import FeestDag
from church_calendar_func import *


class KerkelijkJaarLijst(object):
    paaskring = {-42: ('Invocabit', 'Paars'),
                 -35: ('Reminiscere', 'Paars'),
                 -28: ('Oculi', 'Paars'),
                 -21: ('Laetare', 'Roze'),
                 -14: ('Judica', 'Paars'),
                 -7: ('Palmarum', 'Paars'),
                 -3: ('Witte Donderdag', 'Wit'),
                 -2: ('Goede Vrijdag', 'Zwart'),
                 -1: ('Stille Zaterdag','Paars'),
                 0: ('Pasen', 'Wit'),
                 7: ('Quasimodo Geniti', 'Wit'),
                 14: ('Misericordias Domini', 'Wit'),
                 21: ('Jubilate', 'Wit'),
                 28: ('Cantate', 'Wit'),
                 35: ('Rogate', 'Wit'),
                 39: ('Hemelvaart', 'Wit'),
                 42: ('Exaudi', 'Wit'),
                 49: ('Pinksteren', 'Rood'),
                 56: ('Trinitatis', 'Wit')
                 }

    __begin_delta = -42
    __end_delta = 56
    __days_per_week = 7

    def __init__(self, jaar=None):
        self.jaar = jaar
        self.vierdagen = []
        self.jan1year = date(jaar, 1, 1)
        KerkelijkJaarLijst.week = timedelta(KerkelijkJaarLijst.__days_per_week)
        self.pasen = get_easterdate(self.jan1year)
        self.christmas = date(self.jaar - 1, 12, 25)
        if self.christmas.isoweekday() != 7:  # Sunday
            self.vierdagen.append(FeestDag(self.christmas, 'Kerstmis', 'Wit' ))
        self.church_year_start = get_start_churchyear(self.jan1year)
        self.church_year_end = get_start_churchyear(date(self.jaar + 1, 1, 1)) - timedelta(KerkelijkJaarLijst.__days_per_week)

    def eerste_zondag(self):
        return self.church_year_start

    def laatste_zondag(self):
        return self.church_year_end

    def __bepaal_naam_kleur_zondag(self, datum):
        # Bereken eerst het aantal dagen dat de dag van Pasen af ligt
        # dit kan zowel voor Pasen zijn
        # als erna
        verschil = datum - self.pasen
        numdays = verschil.days

        if min(KerkelijkJaarLijst.paaskring) <= numdays <= max(KerkelijkJaarLijst.paaskring):
            # paaskring is een dictionary van tuples.
            # De key is het aantal dagen verschil met Pasen
            # In iedere tupel staat de naam op element 0
            # de kleur op element 1
            benaming, kleur = KerkelijkJaarLijst.paaskring[numdays][0], KerkelijkJaarLijst.paaskring[numdays][1]
        elif numdays > max(KerkelijkJaarLijst.paaskring):  # Zondagen na Trinitatis
            numweeks = (datum - (self.pasen + timedelta(56))).days / KerkelijkJaarLijst.__days_per_week
            benaming = '%2de Zondag na Trinitatis' % numweeks
            kleur = 'Groen'
        elif (datum - date(self.jaar, 1, 6)).days > 0:  # De datum ligt na Epifanie
            numweeks = (datum - date(self.jaar, 1, 6)).days / KerkelijkJaarLijst.__days_per_week  # aantal weken van Epifanie
            benaming = '%se Zondag na Epifanie' % str(numweeks+1)
            kleur = 'Groen'
        elif datum > self.christmas:  # De datum ligt na Kerstmis
            numweeks = (datum - self.christmas).days / KerkelijkJaarLijst.__days_per_week  # aantal weken van Kerstmis
            benaming = '%se Zondag na Kerst' % str(numweeks+1)
            kleur = 'Wit'
        else: # De datum ligt voor Kerstmis en is dus 1 van de Adventszondagen.
            numweeks = (datum - self.church_year_start).days / 7
            benaming = '%se Zondag van Advent' % str(numweeks + 1) if numweeks != 2 else '3e Zondag van Advent (Gaudete)'
            kleur = 'Paars' if numweeks != 2 else 'Roze'
        return benaming, kleur

    def append(self, datum, benaming, kleur='groen'):
        f = FeestDag(datum, benaming, kleur)
        x = self.vierdagen.index(f)
        if x == 0:
            self.vierdagen.append(FeestDag(datum, benaming, kleur))

    def add_sunday(self, datum):
        # eerst bepaal je de naam en de kleur van de zomdag
        benaming, kleur = self.__bepaal_naam_kleur_zondag(datum)
        self.vierdagen.append(FeestDag(datum, benaming, kleur))

    def __str__(self):
        self.vierdagen.sort()
        hulp = 'Kerkelijk jaar {jaar}\n\n'.format(jaar=self.jaar)
        for i in self.vierdagen:
            hulp += "{dag:<10}\n".format(dag=i)
        return hulp

    def easter(self):
        return self.pasen

    def send2csvwriter(self):
        my_list = [f.day2dict() for f in self.vierdagen]
        return my_list
