Book Borrowing System
# 📚 BookABook - Digital Library Management System

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Django](https://img.shields.io/badge/Django-Backend-092E20.svg?logo=django)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-Styling-38B2AC.svg?logo=tailwind-css)
![HTMX](https://img.shields.io/badge/HTMX-Reactivity-336699.svg)

BookABook is a modern, scalable, and fully responsive Library Management System built to bridge the gap between physical book tracking and digital convenience. Equipped with Smart Loan Rules, Real-time Search, and Contextual Role-Based Access.

## ✨ Core Features

### 🔐 1. Role-Based Access Control (RBAC)
Secure system with distinct privileges for different user types:
* **Administrator (Superuser):** Full system access, including User Management & Account Creation.
* **Librarian (Staff):** Can manage Book Catalogue, Physical Inventory, Loan Approvals, Returns, and Fines.
* **Student (Borrower):** Can explore the catalogue, make loan requests, and monitor personal active/overdue loans via a personalized dashboard.

### 📦 2. Smart Inventory & Barcode Tracking
* **Master-Detail Architecture:** Books are categorized as Master Data, while physical copies (`BookItem`) are tracked individually using unique Barcodes/Book Codes.
* **Real-time Stock Calculation:** The system automatically calculates available stock based on currently active loans and lost/damaged items.

### 🔄 3. Advanced Transaction Engine
* **Contextual Loan Purposes:** Supports both **Regular Borrowing** (Take home based on category rules) and **Classroom Use (KBM)** (Strictly return by midnight).
* **Healthy Friction UX:** Borrowers must explicitly agree to library rules via a commitment form before placing a request.
* **Automated Fine Snapshots:** Penalty rates are locked at the time of borrowing, ensuring financial data integrity even if global penalty rules change in the future.

### ⚡ 4. Blazing Fast UI with HTMX
* **Live Search Capabilities:** Search through Catalogue, Inventory, Loans, and Fines instantly without reloading the page, utilizing HTMX and Django `Q` objects.
* **Seamless Dashboard Rendering:** Partial rendering for sidebar navigation to eliminate jarring page reloads.

## 🛠️ Technology Stack
* **Backend:** Python 3, Django Framework
* **Frontend:** HTML5, Tailwind CSS (via CDN/Standalone), JavaScript (Vanilla)
* **Reactivity:** HTMX
* **Icons:** FontAwesome & Feather Icons

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/bookabook-system.git](https://github.com/yourusername/bookabook-system.git)
   cd bookabook-system

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

3. **Install Dependencies**
     ```bash
     pip install -r requirements.txt

4. **Run Database Migrations:**
     ```Bash
      python manage.py makemigrations
      python manage.py migrate

5. **Create an Administrator Account:**
      ```Bash
      python manage.py createsuperuser
      Run the Development Server:

6. **Run the Server**
    ```bash
    python manage.py runserver
    
7. Open your browser and navigate to http://localhost:8000/
