from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book, Address
from .models import Publisher
from django.db.models import F, Value, FloatField, ExpressionWrapper, OuterRef, Subquery


def index(request):
    return render(request, "bookmodule/index.html")


def list_books(request):
    return render(request, 'bookmodule/list_books.html')


def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')


def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links(request):
    return render(request, 'bookmodule/links.html')

def formatting(request):
    return render(request, 'bookmodule/formatting.html')

def listing(request):
    return render(request, 'bookmodule/listing.html')

def tables(request):
    return render(request, 'bookmodule/tables.html')


def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765, 'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower():
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True
            if contained:
                newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books': newBooks})
    return render(request, 'bookmodule/search.html')


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='Delivery')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})


def complex_query(request):
    mybooks = (
        Book.objects.filter(author__isnull=False)
        .filter(title__icontains='and')
        .filter(edition__gte=2)
        .exclude(price__lte=100)[:10]
    )
    if mybooks:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    return render(request, 'bookmodule/index.html')


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8/books.html', {'books': books, 'task': 1})


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='co') | Q(author__icontains='co'))
    )
    return render(request, 'bookmodule/lab8/books.html', {'books': books, 'task': 2})


def lab8_task3(request):
    # Opposite of the entire Task 2 condition (De Morgan's law).
    books = Book.objects.filter(
        ~(Q(edition__gt=3) & (Q(title__icontains='co') | Q(author__icontains='co')))
    )
    return render(request, 'bookmodule/lab8/books.html', {'books': books, 'task': 3})


def lab8_task4(request):
    books = Book.objects.order_by('title', 'id')
    return render(request, 'bookmodule/lab8/books.html', {'books': books, 'task': 4})


def lab8_task5(request):
    statistics = Book.objects.aggregate(
        count=Count('id'), total=Sum('price', default=0),
        average=Avg('price'), maximum=Max('price'), minimum=Min('price'),
    )
    return render(request, 'bookmodule/lab8/statistics.html', {'statistics': statistics})


def lab8_task7(request):
    cities = Address.objects.values('city').annotate(student_count=Count('students')).order_by('city')
    return render(request, 'bookmodule/lab8/cities.html', {'cities': cities})


def lab9_task1(request):
    total = Book.objects.aggregate(total=Sum('quantity', default=0))['total']
    percentage = ExpressionWrapper(F('quantity') * 100.0 / total, output_field=FloatField()) if total else Value(0.0, output_field=FloatField())
    books = Book.objects.annotate(availability=percentage).select_related('publisher').order_by('title')
    return render(request, 'bookmodule/lab9/results.html', {'task': 1, 'books': books, 'total': total})


def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity', default=0)).order_by('name')
    return render(request, 'bookmodule/lab9/results.html', {'task': 2, 'publishers': publishers})


def lab9_task3(request):
    oldest = Book.objects.filter(publisher=OuterRef('pk')).order_by('pubdate', 'pk')
    publishers = Publisher.objects.annotate(
        oldest_title=Subquery(oldest.values('title')[:1]),
        oldest_date=Min('book__pubdate'),
    ).order_by('name')
    return render(request, 'bookmodule/lab9/results.html', {'task': 3, 'publishers': publishers})


def lab9_task4(request):
    publishers = Publisher.objects.annotate(average=Avg('book__price'), minimum=Min('book__price'), maximum=Max('book__price')).order_by('name')
    return render(request, 'bookmodule/lab9/results.html', {'task': 4, 'publishers': publishers})


def lab9_task5(request):
    highly_rated = Q(book__rating__gte=4)
    publishers = Publisher.objects.annotate(
        high_count=Count('book', filter=highly_rated),
        high_stock=Sum('book__quantity', filter=highly_rated, default=0),
    ).order_by('name')
    return render(request, 'bookmodule/lab9/results.html', {'task': 5, 'publishers': publishers})


def lab9_task6(request):
    publishers = Publisher.objects.annotate(matching_count=Count(
        'book', filter=Q(book__price__gt=50, book__quantity__lt=5, book__quantity__gte=1),
    )).order_by('name')
    return render(request, 'bookmodule/lab9/results.html', {'task': 6, 'publishers': publishers})
