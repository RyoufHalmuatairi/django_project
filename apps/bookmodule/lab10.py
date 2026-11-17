import math

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .forms import BookForm
from .models import Book


def links(part):
    return {
        action: f'books.lab10_part{part}_{action}'
        for action in ('list', 'add', 'edit', 'delete')
    }


@require_safe
def list_books(request, part):
    return render(request, 'bookmodule/lab10/list.html', {
        'part': part,
        'links': links(part),
        'books': Book.objects.order_by('title', 'pk'),
    })


def read_book_fields(post):
    values = {name: post.get(name, '').strip() for name in ('title', 'author', 'price', 'edition')}
    errors = {}
    for name in ('title', 'author'):
        limit = Book._meta.get_field(name).max_length
        if not values[name] or len(values[name]) > limit:
            errors[name] = f'Enter between 1 and {limit} characters.'
    try:
        price = float(values['price'])
        if not math.isfinite(price) or price < 0:
            raise ValueError
    except ValueError:
        errors['price'] = 'Enter a finite price of zero or more.'
    try:
        edition = int(values['edition'])
        if not 1 <= edition <= 32767:
            raise ValueError
    except ValueError:
        errors['edition'] = 'Enter a whole number from 1 to 32767.'
    if errors:
        return values, errors
    return {**values, 'price': price, 'edition': edition}, errors


@require_http_methods(['GET', 'POST'])
def book_editor(request, part, id=None):
    book = get_object_or_404(Book, pk=id) if id is not None else Book()
    routes = links(part)
    context = {'book': book, 'part': part, 'links': routes}
    if part == 2:
        form = BookForm(request.POST if request.method == 'POST' else None, instance=book)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect(routes['list'])
        context['form'] = form
    elif request.method == 'POST':
        values, errors = read_book_fields(request.POST)
        if not errors:
            for field, value in values.items():
                setattr(book, field, value)
            book.save()
            return redirect(routes['list'])
        context.update(values=values, errors=errors)
    else:
        context['values'] = {
            field: getattr(book, field) for field in ('title', 'author', 'price', 'edition')
        }
    return render(request, 'bookmodule/lab10/editor.html', context)


@require_http_methods(['GET', 'POST'])
def delete_book(request, part, id):
    book = get_object_or_404(Book, pk=id)
    routes = links(part)
    if request.method == 'POST':
        book.delete()
        return redirect(routes['list'])
    return render(request, 'bookmodule/lab10/delete.html', {
        'book': book, 'part': part, 'links': routes,
    })
