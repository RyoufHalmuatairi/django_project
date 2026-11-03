from django.test import TestCase
from django.urls import reverse

from .models import Address, Book, Student


class Lab8Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.all().delete()
        cls.books = [
            Book.objects.create(title='CO Networks', author='Ali', price=80, edition=4),
            Book.objects.create(title='Python', author='Cory', price=60, edition=5),
            Book.objects.create(title='Coding', author='Sara', price=81, edition=3),
            Book.objects.create(title='Algorithms', author='Omar', price=120, edition=4),
        ]

    def page(self, task):
        response = self.client.get(reverse(f'books.lab8_task{task}'))
        self.assertEqual(response.status_code, 200)
        return response

    def test_price_includes_boundary(self):
        self.assertEqual(set(self.page(1).context['books']), set(self.books[:2]))

    def test_title_or_author_and_edition(self):
        self.assertEqual(set(self.page(2).context['books']), set(self.books[:2]))

    def test_opposite_query(self):
        matching = set(self.page(2).context['books'])
        opposite = set(self.page(3).context['books'])
        self.assertFalse(matching & opposite)
        self.assertEqual(matching | opposite, set(self.books))

    def test_sorting(self):
        self.assertEqual(list(self.page(4).context['books']), sorted(self.books, key=lambda b: b.title))

    def test_statistics(self):
        self.assertEqual(self.page(5).context['statistics'], {
            'count': 4, 'total': 341, 'average': 85.25, 'maximum': 120, 'minimum': 60,
        })

    def test_empty_database(self):
        Book.objects.all().delete()
        statistics = self.page(5).context['statistics']
        self.assertEqual(statistics['count'], 0)
        self.assertEqual(statistics['total'], 0)
        self.assertIsNone(statistics['average'])
        self.assertContains(self.page(1), 'No matching books.')

    def test_students_grouped_by_city_including_empty_cities(self):
        first = Address.objects.create(city='Riyadh')
        second = Address.objects.create(city='Riyadh')
        Address.objects.create(city='Jeddah')
        Student.objects.create(name='Ahmed', age=20, address=first)
        Student.objects.create(name='Sara', age=21, address=second)
        self.assertEqual(list(self.page(7).context['cities']), [
            {'city': 'Jeddah', 'student_count': 0},
            {'city': 'Riyadh', 'student_count': 2},
        ])

    def test_sample_data_command_is_repeatable(self):
        from django.core.management import call_command
        call_command('seed_lab8', verbosity=0)
        counts = (Book.objects.count(), Address.objects.count(), Student.objects.count())
        call_command('seed_lab8', verbosity=0)
        self.assertEqual(counts, (Book.objects.count(), Address.objects.count(), Student.objects.count()))
