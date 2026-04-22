from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, LibrarianProfile, Category, Book, BookItem, Borrowing, ReturnRecord, ActivityLog

# 1. Register Custom User pakai bawaan Django biar passwordnya tetap ter-enkripsi
admin.site.register(User, UserAdmin)

# 2. Register tabel master dengan tampilan Custom yang Estetik (Pake Decorator)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'fine_per_day')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'publication_year')
    search_fields = ('title', 'isbn', 'author')
    list_filter = ('category', 'publication_year')

@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ('book_code', 'book', 'condition', 'status', 'location')
    search_fields = ('book_code', 'book__title')
    list_filter = ('status', 'condition')

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_item', 'borrow_date', 'due_date', 'status')
    list_filter = ('status',)

# 3. Register sisanya dengan cara simple
admin.site.register(StudentProfile)
admin.site.register(LibrarianProfile)
admin.site.register(ReturnRecord)
admin.site.register(ActivityLog)