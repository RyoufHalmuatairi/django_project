from datetime import datetime
from datetime import timezone as dt_timezone
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.bookmodule.models import Author, Book, Publisher


class Command(BaseCommand):
    help = 'Populate Lab 9 relationships and sample stock without replacing existing books.'

    @transaction.atomic
    def handle(self, *args, **options):
        publishers = []
        for name, location in [('Tech Press', 'Riyadh'), ('Learning House', 'Jeddah'), ('New Publisher', 'Dammam')]:
            publisher, _ = Publisher.objects.get_or_create(name=name, defaults={'location': location})
            publishers.append(publisher)
        for index, book in enumerate(Book.objects.order_by('pk')):
            # Only initialize books that have not yet been assigned a publisher.
            if book.publisher_id is not None:
                continue
            book.publisher = publishers[index % 2]
            book.quantity = [7, 3, 0, 4, 2, 5, 1][index % 7]
            book.rating = [5, 3, 4, 5, 4, 2, 3][index % 7]
            book.pubdate = datetime(2010 + index % 15, 1, 1, tzinfo=dt_timezone.utc)
            book.save(update_fields=['publisher', 'quantity', 'rating', 'pubdate'])
            author, _ = Author.objects.get_or_create(name=book.author or 'Unknown')
            book.authors.add(author)
        self.stdout.write(self.style.SUCCESS('Lab 9 sample data is ready.'))
