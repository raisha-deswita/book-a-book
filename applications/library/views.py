from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Category, Borrowing, User
from .forms import CustomRegisterForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

# Landing Page View
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

# User Registration View
def registration(request):
    if request.user.is_authenticated:
        return redirect('library:dashboard')

    if request.method == 'POST':
        # 2. GUNAKAN FORM BARU DI SINI
        form = CustomRegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student' 
            user.save()

            subject = 'Selamat Datang di BookABook!'
            message = f'Halo {user.username},\n\nTerima kasih sudah mendaftar di sistem perpustakaan BookABook. Akun kamu sudah aktif dan siap digunakan untuk meminjam buku.\n\nSalam,\nAdmin Perpustakaan'
            pengirim = 'no-reply@bookabook.com'
            penerima = [user.email]
            
            # Tembak emailnya!
            send_mail(subject, message, pengirim, penerima)

            return redirect('library:login')
    else:
        form = CustomRegisterForm()

    return render(request, 'library/registration.html', {'form': form})

# Dashboard Views
login_required(login_url='library:login')
def dashboard(request):
    # 1. Dashboard Utama (Base)
    return render(request, 'library/dashboard.html')

@login_required(login_url='library:login')
def dash_home(request):
    # 2. Partial Statistik (Isi konten tengah)
    context = {
        'total_books': Book.objects.count(),
        'total_categories': Category.objects.count(),
        'total_borrowed': Borrowing.objects.filter(status='borrowed').count(),
        'total_students': User.objects.filter(role='student').count(),
    }
    # Perhatikan: kita merender file yang ada di folder partials!
    return render(request, 'library/partials/dash_home.html', context)

# Inventory Views (CRUD Buku, Category)
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    context = {
        'book': book
    }
    return render(request, 'library/book_detail.html', context)

