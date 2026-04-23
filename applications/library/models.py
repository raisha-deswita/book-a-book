from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# 1. CORE AUTHENTICATION & PROFILES

class User(AbstractUser):
    # Menggantikan default User Django. Punya role khusus.
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Null & blank True biar gak error pas bikin superuser awal
    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

# Profil khusus Siswa
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    nisn = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.nisn}"

# Profil khusus Pustakawan
class LibrarianProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='librarian_profile')
    employee_id = models.CharField(max_length=50, unique=True) # NIP
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.position}"


# 2. CATALOGUES (MASTER DATA) & CLASSIFICATION

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    fine_per_day = models.PositiveIntegerField(default=1000) # Pake PositiveIntegerField biar gak ada denda minus

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='books')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    synopsis = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    publication_place = models.CharField(max_length=255, blank=True, null=True)
    page_count = models.IntegerField()
    edition = models.CharField(max_length=50, blank=True, null=True)
    dimensions = models.CharField(max_length=50, blank=True, null=True)
    cover_material = models.CharField(max_length=50, blank=True, null=True)
    
    # Wajib install Pillow untuk ini. upload_to menentukan folder simpanannya.
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 3. PHYSICAL INVENTORY (ITEMS)

class BookItem(models.Model):
    CONDITION_CHOICES = (
        ('good', 'Good'),
        ('slightly_damaged', 'Slightly Damaged'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('maintenance', 'Maintenance'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='items')
    book_code = models.CharField(max_length=50, unique=True) # Barcode spesifik per buku
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=100, blank=True, null=True) # Misal: "Rak A3"

    class Meta:
        verbose_name = "Physical Book Item"
        verbose_name_plural = "Physical Book Items"

    def __str__(self):
        return f"{self.book_code} - {self.book.title}"


# 4. TRANSACTIONAL DATA (BORROW & RETURN)

class Borrowing(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('active', 'Active (Borrowed)'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )
    
    # Siapa yang pinjam?
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='borrowings')
    
    # Buku fisik mana yang dipinjam?
    book_item = models.ForeignKey(BookItem, on_delete=models.RESTRICT, related_name='borrowings')
    
    # Siapa petugas yang ACC/Ngasih bukunya? (Niru konsep Pra-UKK, penting!)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_borrowings')

    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    
    # [SNAPSHOT TECHNIQUE] - Simpan denda saat ini biar kalau kategori berubah, denda lama gak error.
    fine_snapshot = models.PositiveIntegerField(default=0, help_text="Snapshot of fine per day when borrowed")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)

    # Otomatisasi Snapshot Denda sebelum di-save ke DB
    def save(self, *args, **kwargs):
        if not self.pk: # Kalau ini adalah data baru dibuat
            self.fine_snapshot = self.book_item.book.category.fine_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book_item.book_code}"

class ReturnRecord(models.Model):
    FINE_STATUS_CHOICES = (
        ('not_applicable', 'No Fine'),
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    )
    
    # Relasi 1-to-1 dengan Borrowing. 1 peminjaman = 1 pengembalian.
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE, related_name='return_record')
    
    # Petugas yang menerima buku kembalian
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_returns')
    
    return_date = models.DateTimeField(auto_now_add=True)
    late_days = models.PositiveIntegerField(default=0)
    total_fine = models.PositiveIntegerField(default=0)
    fine_status = models.CharField(max_length=20, choices=FINE_STATUS_CHOICES, default='not_applicable')
    
    # Kondisi buku saat dikembalikan (biar petugas bisa ngecek)
    return_condition = models.CharField(max_length=20, choices=BookItem.CONDITION_CHOICES, default='good')

    def __str__(self):
        return f"Return for {self.borrowing}"


# 5. SYSTEM LOGS

class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Soft Delete: Data disembunyikan, bukan dihancurkan
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp'] # Otomatis urut dari yang paling baru ke lama
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    # Method sakti untuk memicu soft delete
    def soft_delete(self):
        self.is_deleted = True
        self.save()