from django.shortcuts import render
from .models import Book, Category

def index(request):
    # Ambil 6 buku terbaru
    recent_books = Book.objects.select_related('category').order_by('-created_at')[:6]
    categories = Category.objects.all()

    # Bungkus datanya ke dalam dictionary context
    context = {
        'recent_books': recent_books,
        'categories': categories,
    }
    
    # Lempar datanya ke file HTML
    return render(request, 'library/index.html', context)