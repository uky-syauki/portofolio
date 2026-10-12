# Aurora — Flask Starter dengan Modern UI/UX

Starter project Python + Flask dengan tampilan modern: glassmorphism, gradient,
dark mode, animasi scroll-reveal, dan fully responsive. Tanpa build step —
tinggal clone, install, dan jalan.

## Fitur

- 🎨 **Modern UI/UX** — gradient hero, glass cards, hover micro-interactions
- 🌙 **Dark mode** — toggle dengan preferensi tersimpan di `localStorage`
- 📱 **Responsive** — navbar hamburger, grid adaptif untuk semua ukuran layar
- 🧭 **Halaman** — Home (hero, features, products, testimonials, CTA) + About + 404
- 🔌 **API JSON** — `/api/products`, `/api/health`
- 🏭 **App factory pattern** — mudah diuji dan dikembangkan

## Struktur Proyek

```
.
├── app.py                  # Flask app + routes + sample data
├── requirements.txt
├── templates/
│   ├── base.html           # Layout dasar (theme, fonts, import macro)
│   ├── index.html          # Landing page
│   ├── about.html          # About page
│   ├── 404.html            # Error page
│   └── partials/
│       └── _macros.html    # Navbar & footer reusable
└── static/
    ├── css/style.css       # Design system (CSS variables, dark mode)
    └── js/main.js          # Theme toggle, mobile nav, scroll reveal
```

## Menjalankan

```bash
# 1. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependency
pip install -r requirements.txt

# 3. Jalankan server
python app.py
```

Buka http://127.0.0.1:5000 🎉

Atau modus khas Flask:

```bash
flask --app app run --debug
```

## Customization

- **Warna & tema** — ubah CSS variables di bagian `:root` pada
  `static/css/style.css` (primary, accent, gradient, radius, dll).
- **Konten** — data products/features/testimonials ada di `app.py`; pindahkan
  ke database bila perlu.
- **Halaman baru** — buat template yang `{% extends "base.html" %}`, lalu
  tambahkan route di `app.py` dan link di `partials/_macros.html`.

## Endpoint API

| Endpoint        | Deskripsi                          |
| --------------- | ---------------------------------- |
| `GET /`         | Landing page                       |
| `GET /about`    | About page                         |
| `GET /api/products?category=Audio` | Daftar produk dari SQLite (filter opsional) |
| `GET /api/health` | Health check                     |

## Database

Produk kini disimpan di **SQLite** (`products.db`, dibuat otomatis saat app
pertama dijalankan, lengkap dengan seed data). Helper ada di `db.py`:

- `get_db()` — koneksi SQLite per-request (otomatis ditutup)
- `init_db()` — buat schema + seed data (idempotent)
- `query_products(category=None)` — ambil produk, filter kategori opsional

Contoh query langsung:

```bash
sqlite3 products.db "SELECT name, price FROM products;"
```
