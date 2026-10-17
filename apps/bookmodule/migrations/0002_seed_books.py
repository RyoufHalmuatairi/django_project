from django.db import migrations


BOOKS = [
    ('Continuous Delivery', 'J.Humble and D. Farley', 120.00, 3),
    ('Reversing: Secrets of Reverse Engineer', 'E. Eilam', 97.00, 2),
    ('The Hundred-Page Machine Learning Book', 'Andriy Burkov', 100.00, 4),
]


def seed_books(apps, schema_editor):
    Book = apps.get_model('bookmodule', 'Book')
    for title, author, price, edition in BOOKS:
        Book.objects.update_or_create(
            title=title,
            defaults={'author': author, 'price': price, 'edition': edition},
        )


def remove_seed_books(apps, schema_editor):
    Book = apps.get_model('bookmodule', 'Book')
    Book.objects.filter(title__in=[book[0] for book in BOOKS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('bookmodule', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_books, remove_seed_books),
    ]
