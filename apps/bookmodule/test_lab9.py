from datetime import datetime, timezone
from django.test import TestCase
from django.urls import reverse
from .models import Book, Publisher, Author


class Lab9Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.all().delete()
        cls.publisher = Publisher.objects.create(name='Test Press', location='Riyadh')
        cls.empty = Publisher.objects.create(name='Empty Press', location='Jeddah')
        cls.old = Book.objects.create(title='Old', author='Ali', price=60, quantity=3, rating=4,
            pubdate=datetime(2000, 1, 1, tzinfo=timezone.utc), publisher=cls.publisher)
        Book.objects.create(title='New', author='Sara', price=100, quantity=7, rating=3,
            pubdate=datetime(2020, 1, 1, tzinfo=timezone.utc), publisher=cls.publisher)
        cls.old.authors.add(Author.objects.create(name='Ali'), Author.objects.create(name='Sara'))

    def page(self, task):
        response = self.client.get(reverse(f'books.lab9_task{task}'))
        self.assertEqual(response.status_code, 200)
        return response

    def publisher_result(self, task):
        return self.page(task).context['publishers'].get(pk=self.publisher.pk)

    def test_availability_annotation_is_not_saved(self):
        books = self.page(1).context['books']
        self.assertEqual(books.get(pk=self.old.pk).availability, 30)
        self.assertNotIn('availability', [field.name for field in Book._meta.fields])

    def test_zero_stock_and_empty_books(self):
        Book.objects.update(quantity=0)
        self.assertTrue(all(book.availability == 0 for book in self.page(1).context['books']))
        Book.objects.all().delete()
        self.assertContains(self.page(1), 'No books available.')

    def test_stock_and_empty_publisher(self):
        self.assertEqual(self.publisher_result(2).total_stock, 10)
        self.assertEqual(self.page(2).context['publishers'].get(pk=self.empty.pk).total_stock, 0)

    def test_oldest_book(self):
        self.assertEqual(self.publisher_result(3).oldest_title, 'Old')
        self.assertIsNone(self.page(3).context['publishers'].get(pk=self.empty.pk).oldest_title)

    def test_prices(self):
        result = self.publisher_result(4)
        self.assertEqual((result.average, result.minimum, result.maximum), (80, 60, 100))

    def test_high_ratings(self):
        result = self.publisher_result(5)
        self.assertEqual((result.high_count, result.high_stock), (1, 3))

    def test_filter_boundaries(self):
        for price, quantity in [(50, 3), (60, 0), (60, 5), (60, 1), (60, 4)]:
            Book.objects.create(title='Boundary', price=price, quantity=quantity, publisher=self.publisher)
        self.assertEqual(self.publisher_result(6).matching_count, 3)

    def test_publisher_deletion_keeps_books(self):
        self.publisher.delete()
        self.old.refresh_from_db()
        self.assertIsNone(self.old.publisher_id)

    def test_seed_is_repeatable(self):
        from django.core.management import call_command
        call_command('seed_lab9')
        counts = (Book.objects.count(), Publisher.objects.count(), Author.objects.count(), Book.authors.through.objects.count())
        call_command('seed_lab9')
        self.assertEqual(counts, (Book.objects.count(), Publisher.objects.count(), Author.objects.count(), Book.authors.through.objects.count()))
