# Detik.com Article Scraper

A Python scraper to fetch search results from [Detik.com](https://www.detik.com/). This script allows you to retrieve article details including title, image link, body text, and publication time, while skipping advertisements.

---

## 🛠️ Teknologi

* **Backend / Language:** Python 3.x
* **Libraries:** `requests`, `BeautifulSoup4`
* **Output Format:** JSON

---

## ⚡ Fitur

* Search Detik.com articles using a query string.
* Supports pagination (up to 3 pages per search).
* Skips advertisements (e.g., elements with `.ads-slot-mb-container`).
* Handles missing data gracefully (e.g., missing body text).
* Saves results to JSON file.
* Implements basic error handling for network issues, invalid responses, and missing data.

---

## 📦 Instalasi

1. Clone repository:

```bash
git clone https://github.com/Aryaaazrr/web-scrapping-for-news-article.git
cd web-scrapping-for-news-article
```

2. Install dependencies:

```bash
pip install requests
pip install beautifulsoup4
```

---

## 🚀 Cara Penggunaan

1. Jalankan script Python:

```bash
python main.py
```

2. Masukkan search query ketika diminta.
   Default: `teknologi`

3. Masukkan jumlah halaman yang ingin di-scrape (1–3).
   Default: 3

4. Script akan menampilkan hasil di console dan menyimpan data ke file JSON:

```
detik_search_<query>.json
```

---

## ⚠️ Contoh Output JSON

```json
{
    "title": "Sosok Affan Kurniawan, Driver Ojol yang Tewas Dilindas Rantis Polisi",
    "image_link": "https://akcdn.detik.net.id/community/media/visual/2025/08/29/jenazah-affan-kurniawan-tiba-di-rumah-duka-taufiqdetikcom-1756412581598_43.jpeg?w=250&q=90",
    "body_text": "Pengemudi ojol Affan Kurniawan tewas dilindas rantis Brimob saat demo di Jakarta. Keluarga merasa kehilangan sosok rajin dan tulang punggung keluarga.",
    "publication_time": "17 menit yang lalu"
}
```

---

## 📌 Catatan

* Pastikan koneksi internet stabil saat menjalankan scraper.
* Hanya scrape artikel publik, jangan melakukan scraping berlebihan agar tidak diblokir.

---

## 📝 Lisensi

Project ini bersifat open-source. Silakan digunakan dan dikembangkan sesuai kebutuhan.
