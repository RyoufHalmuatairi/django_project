from django.core.management.base import BaseCommand
from django.db import transaction

from apps.bookmodule.models import Address, Book, Student


class Command(BaseCommand):
    help = 'Add reusable sample books, addresses and students for Lab 8.'

    @transaction.atomic
    def handle(self, *args, **options):
        books = [
            ('Computer Networks', 'Andrew Tanenbaum', 80, 5),
            ('Python Basics', 'Cory Smith', 65, 4),
            ('Coding Essentials', 'Sara Ali', 50, 3),
            ('Database Systems', 'Omar Ahmed', 95, 5),
        ]
        for title, author, price, edition in books:
            Book.objects.get_or_create(title=title, defaults={
                'author': author, 'price': price, 'edition': edition,
            })
        for city, students in [
            ('Riyadh', [('Ahmed', 20), ('Sara', 21)]),
            ('Jeddah', [('Omar', 22)]),
            ('Buraydah', [('Noura', 20), ('Khalid', 23), ('Hind', 21)]),
            ('Dammam', []),
        ]:
            address = Address.objects.filter(city=city).first()
            if address is None:
                address = Address.objects.create(city=city)
            for name, age in students:
                Student.objects.get_or_create(name=name, address=address, defaults={'age': age})
        self.stdout.write(self.style.SUCCESS('Lab 8 sample data is ready.'))
