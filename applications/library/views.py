from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookItem, Category, Borrowing, User, ReturnRecord
from .forms import CustomRegisterForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q

# CRUD management user (superuser/admin only)
@login_required(login_url='library:login')
def user_management(request):
    # 🛡️ PROTEKSI: CUMA SUPERUSER YANG BOLEH MASUK!
    if not request.user.is_superuser:
        messages.error(request, "Akses Ilegal! Anda bukan Admin.")
        return redirect('library:dash_home')
        
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'library/user_management.html', {'users': users})

@login_required(login_url='library:login')
def user_add(request):
    if not request.user.is_superuser:
        return redirect('library:dash_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role', 'student')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        
        # Cek apakah username sudah dipakai
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' sudah digunakan!")
            return redirect('library:user_add')

        # Create user menggunakan create_user biar passwordnya di-hash (dienkripsi)
        new_user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
            role=role, phone_number=phone, address=address
        )
        
        # Atur otorisasi Django berdasarkan role
        if role == 'admin':
            new_user.is_staff = True
            new_user.is_superuser = True
        elif role == 'librarian':
            new_user.is_staff = True
            new_user.is_superuser = False
        else:
            new_user.is_staff = False
            new_user.is_superuser = False
            
        new_user.save()
        messages.success(request, f"Akun '{username}' berhasil dibuat dengan role {role.upper()}!")
        return redirect('library:user_management')
        
    return render(request, 'library/user_form.html', {'action': 'Add New'})

@login_required(login_url='library:login')
def user_edit(request, user_id):
    if not request.user.is_superuser:
        return redirect('library:dash_home')

    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        target_user.username = request.POST.get('username')
        target_user.email = request.POST.get('email')
        target_user.first_name = request.POST.get('first_name')
        target_user.last_name = request.POST.get('last_name')
        target_user.phone_number = request.POST.get('phone_number')
        target_user.address = request.POST.get('address')
        
        role = request.POST.get('role')
        target_user.role = role
        
        # Atur otorisasi Django berdasarkan role
        if role == 'admin':
            target_user.is_staff = True
            target_user.is_superuser = True
        elif role == 'librarian':
            target_user.is_staff = True
            target_user.is_superuser = False
        else:
            target_user.is_staff = False
            target_user.is_superuser = False
            
        # Update password HANYA kalau diisi (kalau kosong, biarkan password lama)
        new_password = request.POST.get('password')
        if new_password:
            target_user.set_password(new_password)
            
        target_user.save()
        messages.success(request, f"Data akun '{target_user.username}' diperbarui!")
        return redirect('library:user_management')
        
    return render(request, 'library/user_form.html', {'target_user': target_user, 'action': 'Edit'})

@login_required(login_url='library:login')
def user_delete(request, user_id):
    if not request.user.is_superuser:
        return redirect('library:dash_home')

    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        
        # Cegah Admin Hapus Dirinya Sendiri! (Biar gak konyol wkwk)
        if target_user == request.user:
            messages.error(request, "Kamu tidak bisa menghapus akunmu sendiri!")
        else:
            username = target_user.username
            target_user.delete()
            messages.warning(request, f"Akun '{username}' telah dimusnahkan.")
            
    return redirect('library:user_management')

def index(request):
    query = request.GET.get('q')

    # 1. Logika Filter Dulu
    if query:
        recent_books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).distinct() # Pake distinct biar ga ada data ganda
    else:
        recent_books = Book.objects.all().order_by('-id')[:6]
        
    # 2. BARU BUNGKUS KE CONTEXT
    context = {
        'recent_books': recent_books,
        'categories': Category.objects.all(),
    }

    # 🌟 3. MAGIC HTMX: Kalau yang nge-request adalah ketikan Live Search
    if request.headers.get('HX-Request'):
        # Balikin POTONGAN grid bukunya aja, jangan satu halaman full!
        return render(request, 'library/partials/book_grid.html', context)

    # 4. Kalau request biasa (pertama kali buka web)
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
    # Dashboard Utama (Base)
    return render(request, 'library/dashboard.html')

@login_required(login_url='library:login')
def dash_home(request):
    # 🌟 1. HITUNG STATISTIK GLOBAL
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_borrowed = Borrowing.objects.filter(status='active').count()
    total_students = User.objects.filter(role='student').count()

    # 🌟 2. TARIK 3 BUKU TERBARU (Untuk Widget 'Recent Additions')
    recent_additions = Book.objects.order_by('-created_at')[:3]

    # 🌟 3. TARIK DATA TRANSAKSI (Sesuai Hak Akses)
    if request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian':
        # Kalau Admin/Librarian: Lihat semua antrean
        pending_loans = Borrowing.objects.filter(status='pending').order_by('borrow_date')
        active_loans = Borrowing.objects.filter(status='active').order_by('due_date')
    else:
        # Kalau Student: Gak usah lihat antrean orang lain
        pending_loans = Borrowing.objects.filter(user=request.user, status='pending').order_by('borrow_date')
        active_loans = Borrowing.objects.filter(user=request.user, status='active').order_by('due_date')

    # 🌟 4. BUNGKUS SEMUA KE CONTEXT
    context = {
        'total_books': total_books,
        'total_categories': total_categories,
        'total_borrowed': total_borrowed,
        'total_students': total_students,
        'recent_additions': recent_additions,
        'pending_loans': pending_loans,
        'active_loans': active_loans,
        'now': timezone.now(), # PENTING! Buat ngecek overdue di HTML
    }

    # Render sesuai arsitektur HTMX kita
    if request.headers.get('HX-Request'):
        return render(request, 'library/partials/dash_home.html', context)
    else:
        return render(request, 'library/dash_home_full.html', context)

# Inventory Views (CRUD Buku, Category)
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    user_has_loan = False
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'student':
        user_has_loan = Borrowing.objects.filter(
            user=request.user,
            book_item__book=book,
            status__in=['pending', 'active'] # Kalau masih pending/dipinjam, true!
        ).exists()

    context = {
        'book': book,
        'user_has_loan': user_has_loan, # Kirim ke HTML
    }
    return render(request, 'library/book_detail.html', context)

# Transaction Views (Borrow, Approval, Return)
@login_required(login_url='library:login')
def request_borrow(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        
        available_item = BookItem.objects.filter(book=book, status='available').first()
        
        if not available_item:
            messages.error(request, "Sorry, all copies of this book are currently unavailable.")
            return redirect('library:book_detail', book_id=book.id)
            
        # 🌟 1. TANGKAP TIPE PEMINJAMAN DARI MODAL HTML
        loan_type = request.POST.get('loan_type', 'reguler')
        
        # 🌟 2. TARIK ATURAN DINAMIS DARI KATEGORI BUKU
        kategori_buku = book.category
        jatah_hari = kategori_buku.loan_duration_days
        tarif_denda = kategori_buku.fine_per_day
        
        tanggal_sekarang = timezone.now()
        
        # 🌟 3. LOGIKA DUE DATE PINTAR (KBM vs REGULER)
        if loan_type == 'kbm':
            # Balik hari ini juga jam 23:59:59
            due_date = tanggal_sekarang.replace(hour=23, minute=59, second=59)
        else:
            # Sesuai aturan kategori (misal: Novel 7 hari, Buku Paket 14 hari)
            due_date = tanggal_sekarang + timedelta(days=jatah_hari)
        
        # 🌟 4. SIMPAN KE DATABASE (Jangan lupa fine_snapshot!)
        Borrowing.objects.create(
            user=request.user,
            book_item=available_item,
            borrow_date=tanggal_sekarang,
            due_date=due_date,
            status='pending',
            fine_snapshot=tarif_denda  # <--- CRITICAL: Biar dendanya kekunci!
        )
        
        available_item.status = 'maintenance'
        available_item.save()
        
        messages.success(request, f"Borrowing request submitted! Please wait for approval from the librarian.")
        # Note: Boleh ganti redirect ke 'library:dashboard' kalau user-nya student, biar dia nggak bingung.
        return redirect('library:dashboard')
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        
        available_item = BookItem.objects.filter(book=book, status='available').first()
        
        if not available_item:
            messages.error(request, "Sorry, all copies of this book are currently unavailable.")
            return redirect('library:book_detail', book_id=book.id)
            
        due_date = timezone.now() + timedelta(days=7)
        
        Borrowing.objects.create(
            user=request.user,
            book_item=available_item,
            due_date=due_date,
            status='pending'
        )
        
        available_item.status = 'maintenance'
        available_item.save()
        
        messages.success(request, "Borrowing request has been submitted! Please wait for approval from the librarian.")
        return redirect('library:loan_management')
    
@login_required(login_url='library:login')
def process_borrow_request(request, borrowing_id, action):
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)
    book_item = borrowing.book_item
    
    if action == 'approve':
        borrowing.status = 'active'
        borrowing.approved_by = request.user
        borrowing.save()
        
        book_item.status = 'borrowed'
        book_item.save()
        
        messages.success(request, f"ACC Sukses! Buku {book_item.book_code} resmi dibawa pulang.")
        
    elif action == 'reject':
        borrowing.delete()
        
        book_item.status = 'available'
        book_item.save()
        
        messages.warning(request, "Permintaan ditolak. Fisik buku dikembalikan ke status Tersedia.")

    return redirect('library:loan_management')

# Return Process
@login_required(login_url='library:login')
def return_book(request, borrowing_id):
    if request.method == 'POST':
        borrowing = get_object_or_404(Borrowing, id=borrowing_id)
        book_item = borrowing.book_item
        
        # menghitung keterlambatan
        now = timezone.now()
        late_days = 0
        total_fine = 0
        fine_status = 'not_applicable'
        
        if now > borrowing.due_date:
            # selisih hari
            delta = now - borrowing.due_date
            late_days = delta.days + (1 if delta.seconds > 0 else 0)
            
            # hitung denda
            total_fine = late_days * borrowing.fine_snapshot
            fine_status = 'unpaid' if total_fine > 0 else 'not_applicable'

        # simpan data
        ReturnRecord.objects.create(
            borrowing=borrowing,
            received_by=request.user,
            late_days=late_days,
            total_fine=total_fine,
            fine_status=fine_status,
            return_condition=request.POST.get('condition', 'good')
        )

        # update status peminjaman
        borrowing.status = 'returned'
        borrowing.save()
        
        # update status book availability
        book_item.status = 'available'
        
        # update book condition based on returned condition
        book_item.condition = request.POST.get('condition', 'good')
        book_item.save()

        messages.success(request, f"Buku {book_item.book_code} berhasil dikembalikan! Denda: Rp{total_fine}")
        return redirect('library:dashboard')

@login_required(login_url='library:login')
def loan_management(request):
    query = request.GET.get('q')
    
    # 🌟 1. TARIK DATA DASAR BERDASARKAN ROLE
    if request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian':
        base_loans = Borrowing.objects.all()
    else:
        base_loans = Borrowing.objects.filter(user=request.user)
        
    # 🌟 2. TIMPA DENGAN FILTER PENCARIAN (Kalau ada ketikan)
    if query:
        loans = base_loans.filter(
            Q(user__username__icontains=query) | 
            Q(book_item__book__title__icontains=query) |
            Q(book_item__book_code__icontains=query)
        ).distinct().order_by('-borrow_date')
    else:
        loans = base_loans.order_by('-borrow_date')
        
    context = {
        'loans': loans,
    }

    # 🌟 3. LOGIKA RENDER (Sama kayak sebelumnya)
    if request.headers.get('HX-Request'):
        return render(request, 'library/partials/loan_management.html', context)
    else:
        return render(request, 'library/loan_management_full.html', context)

@login_required
def dashboard_book_list(request):
    query = request.GET.get('q')
    
    # 🌟 LOGIKA LIVE SEARCH
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        books = Book.objects.all().order_by('-created_at')
        
    context = {'books': books}
    
    # Tetap pakai logika Interceptor yang udah kita benerin tadi
    if request.headers.get('HX-Request'):
        return render(request, 'library/partials/book_list_dashboard.html', context)
    else:
        # (Sesuaikan dengan nama file wrapper utama dashboard kamu)
        return render(request, 'library/inventory_full.html', context)
    
# fine management
@login_required(login_url='library:login')
def fine_management(request):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')
    
    query = request.GET.get('q')
    
    # 🌟 1. TARIK SEMUA DATA YANG ADA DENDANYA (Lunas & Belum Lunas)
    base_fines = ReturnRecord.objects.exclude(fine_status='not_applicable')
    
    # 🌟 2. LOGIKA LIVE SEARCH
    if query:
        fines = base_fines.filter(
            Q(borrowing__user__username__icontains=query) |
            Q(borrowing__book_item__book__title__icontains=query) |
            Q(borrowing__book_item__book_code__icontains=query)
        ).distinct().order_by('-return_date')
    else:
        fines = base_fines.order_by('-return_date')
    
    # Namanya aku ganti jadi 'fines' aja biar universal (karena isinya gabungan)
    context = {
        'fines': fines,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'library/partials/fine_management.html', context)
    else:
        return render(request, 'library/fine_management_full.html', context)

@login_required(login_url='library:login')
def pay_fine(request, record_id):
    if request.method == 'POST':
        # Cari data dendanya
        record = get_object_or_404(ReturnRecord, id=record_id)
        
        # Ubah status jadi LUNAS!
        record.fine_status = 'paid'
        record.save()
        
        # Kembali ke halaman kasir
        return redirect('library:fine_management')
    
# Inventarisasi Buku (CRUD)

# 1. TAMBAH BUKU
@login_required(login_url='library:login')
def book_add(request):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        messages.error(request, "Akses Ilegal! Anda bukan Pustakawan.")
        return redirect('library:dash_home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        synopsis = request.POST.get('synopsis')
        cover = request.FILES.get('cover_image')
        
        # Field Tambahan
        pub_year = request.POST.get('publication_year')
        pub_place = request.POST.get('publication_place')
        pages = request.POST.get('page_count')
        edition = request.POST.get('edition')
        dimensions = request.POST.get('dimensions')
        cover_material = request.POST.get('cover_material')
        
        category = get_object_or_404(Category, id=category_id)
        
        Book.objects.create(
            title=title, category=category, author=author,
            isbn=isbn, publisher=publisher, synopsis=synopsis,
            cover_image=cover,
            publication_year=pub_year, publication_place=pub_place,
            page_count=pages, edition=edition, 
            dimensions=dimensions, cover_material=cover_material
        )
        messages.success(request, f"Buku '{title}' berhasil ditambahkan!")
        return redirect('library:inventory_management') 
    
    categories = Category.objects.all()
    return render(request, 'library/book_form_full.html', {
        'categories': categories, 
        'action': 'Add New'
    })

# 2. EDIT BUKU
@login_required(login_url='library:login')

def book_edit(request, book_id):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        messages.error(request, "Akses Ilegal! Anda bukan Pustakawan.")
        return redirect('library:dash_home')
    
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.publisher = request.POST.get('publisher')
        book.synopsis = request.POST.get('synopsis')
        book.category = get_object_or_404(Category, id=request.POST.get('category'))
        
        # Field Tambahan
        book.publication_year = request.POST.get('publication_year')
        book.publication_place = request.POST.get('publication_place')
        book.page_count = request.POST.get('page_count')
        book.edition = request.POST.get('edition')
        book.dimensions = request.POST.get('dimensions')
        book.cover_material = request.POST.get('cover_material')
        
        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES.get('cover_image')
            
        book.save()
        messages.success(request, f"Data buku '{book.title}' diperbarui!")
        return redirect('library:inventory_management')
    
    categories = Category.objects.all()
    return render(request, 'library/book_form_full.html', {
        'book': book, 
        'categories': categories, 
        'action': 'Edit'
    })

# 3. HAPUS BUKU
@login_required(login_url='library:login')
def book_delete(request, book_id):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        messages.error(request, "Akses Ilegal! Anda bukan Pustakawan.")
        return redirect('library:dash_home')
    # Gunakan POST untuk hapus data (Security Best Practice)
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        title = book.title
        book.delete()
        messages.warning(request, f"Buku '{title}' telah dihapus.")
    
    # FIX: Redirect ke Nama URL
    return redirect('library:inventory_management')

# applications/library/views.py

@login_required(login_url='library:login')
def inventory_management(request):
    # Pastikan nama fungsinya EXACTLY 'inventory_management' (huruf kecil semua)
    books = Book.objects.all().order_by('-id')
    
    context = {
        'books': books,
    }

    # Cek apakah ini permintaan HTMX
    if request.headers.get('HX-Request'):
        # Manggil file partial yang berisi kartu-kartu buku
        return render(request, 'library/partials/book_list_dashboard.html', context)
    else:
        # Manggil file wrapper full
        return render(request, 'library/inventory_full.html', context)
    
@login_required(login_url='library:login')
def category_management(request):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        messages.error(request, "Akses Ilegal!")
        return redirect('library:dash_home')
        
    categories = Category.objects.all().order_by('-id')
    return render(request, 'library/category_management.html', {'categories': categories})

@login_required(login_url='library:login')
def category_add(request):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')

    if request.method == 'POST':
        name = request.POST.get('name')
        loan_duration = request.POST.get('loan_duration_days', 7)
        fine = request.POST.get('fine_per_day', 2000)
        
        Category.objects.create(
            name=name, 
            loan_duration_days=loan_duration, 
            fine_per_day=fine
        )
        messages.success(request, f"Kategori '{name}' berhasil ditambahkan!")
        return redirect('library:category_management')
        
    return render(request, 'library/category_form.html', {'action': 'Add New'})

@login_required(login_url='library:login')
def category_edit(request, cat_id):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')

    category = get_object_or_404(Category, id=cat_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.loan_duration_days = request.POST.get('loan_duration_days')
        category.fine_per_day = request.POST.get('fine_per_day')
        category.save()
        
        messages.success(request, f"Kategori '{category.name}' berhasil diperbarui!")
        return redirect('library:category_management')
        
    return render(request, 'library/category_form.html', {'category': category, 'action': 'Edit'})

@login_required(login_url='library:login')
def category_delete(request, cat_id):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')

    if request.method == 'POST':
        category = get_object_or_404(Category, id=cat_id)
        name = category.name
        # Note: Karena di models.py kamu pakai on_delete=models.RESTRICT, 
        # ini bakal error kalau ada buku yang pake kategori ini. Itu bagus! (Mencegah data yatim piatu).
        try:
            category.delete()
            messages.warning(request, f"Kategori '{name}' dihapus.")
        except Exception as e:
            messages.error(request, f"Gagal menghapus! Kategori '{name}' masih dipakai oleh buku.")
            
    return redirect('library:category_management')

@login_required(login_url='library:login')
def book_items_manage(request, book_id):
    # 🛡️ Satpam Lapis Kedua
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')

    book = get_object_or_404(Book, id=book_id)
    items = book.items.all().order_by('-id')

    if request.method == 'POST':
        book_code = request.POST.get('book_code')
        condition = request.POST.get('condition', 'good')
        status = request.POST.get('status', 'available')
        location = request.POST.get('location')

        # 🌟 FITUR DEWA: Cek biar Barcode nggak bentrok!
        if BookItem.objects.filter(book_code=book_code).exists():
            messages.error(request, f"Gagal! Barcode '{book_code}' sudah dipakai di buku lain.")
        else:
            BookItem.objects.create(
                book=book,
                book_code=book_code,
                condition=condition,
                status=status,
                location=location
            )
            messages.success(request, f"Stok fisik dengan barcode '{book_code}' berhasil ditambahkan!")
        
        return redirect('library:book_items_manage', book_id=book.id)

    return render(request, 'library/book_items_manage.html', {
        'book': book,
        'items': items
    })

@login_required(login_url='library:login')
def book_item_edit(request, item_id):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')

    item = get_object_or_404(BookItem, id=item_id)
    
    if request.method == 'POST':
        new_code = request.POST.get('book_code')
        
        # Cek bentrok barcode kalau barcode-nya diubah
        if new_code != item.book_code and BookItem.objects.filter(book_code=new_code).exists():
            messages.error(request, f"Gagal! Barcode '{new_code}' sudah terdaftar.")
        else:
            item.book_code = new_code
            item.condition = request.POST.get('condition')
            item.status = request.POST.get('status')
            item.location = request.POST.get('location')
            item.save()
            messages.success(request, f"Data fisik '{item.book_code}' diperbarui!")
            return redirect('library:book_items_manage', book_id=item.book.id)

    return render(request, 'library/book_item_form.html', {'item': item})

@login_required(login_url='library:login')
def book_item_delete(request, item_id):
    if not (request.user.is_superuser or request.user.is_staff or getattr(request.user, 'role', '') == 'librarian'):
        return redirect('library:dash_home')

    if request.method == 'POST':
        item = get_object_or_404(BookItem, id=item_id)
        book_id = item.book.id
        code = item.book_code
        item.delete()
        messages.warning(request, f"Buku fisik '{code}' telah dihapus dari sistem.")
        return redirect('library:book_items_manage', book_id=book_id)