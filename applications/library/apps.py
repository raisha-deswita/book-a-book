from django.apps import AppConfig

class LibraryConfig(AppConfig): # <-- Namanya bisa disesuaikan juga
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.library'  # <--- Ganti jadi library