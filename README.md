#  Analisis Kebiasaan Begadang & Konsentrasi Mahasiswa ITSB Angkatan 25
### Kelompok 7 — Mata Kuliah Sampling dan Survei | S1 Sains Data ITSB

---

## Deskripsi Proyek

Penelitian ini menganalisis **pengaruh kebiasaan begadang terhadap konsentrasi dan performa akademik mahasiswa Institut Teknologi Sains Bandung (ITSB) Angkatan 25** melalui pendekatan survei kuantitatif. Data dikumpulkan menggunakan Google Forms dan diolah secara statistik dengan Python.

---

## Tujuan Penelitian

| # | Tujuan |
|---|--------|
| 1 | Mengetahui **pola kebiasaan begadang** mahasiswa ITSB Angkatan 25 (durasi tidur, frekuensi, jam tidur) |
| 2 | Mengukur **dampak begadang terhadap konsentrasi dan performa akademik** mahasiswa ITSB Angkatan 25 (fokus, ngantuk, daya ingat, nilai) |
| 3 | Mengidentifikasi **faktor penyebab utama** kebiasaan begadang mahasiswa ITSB Angkatan 25 |
| 4 | Menilai **tingkat kesadaran mahasiswa ITSB Angkatan 25** tentang dampak begadang dan keinginan mengubah pola tidur |

---

## Hasil Utama

### Data Responden
- **Total responden:** 69 orang (mahasiswa ITSB Angkatan 25)
- **Jumlah variabel:** 25 kolom
- **Data duplikat:** 0

### Statistik Deskriptif (Skala 1–5)

| Variabel | Mean | Median | Std Dev | Min | Max |
|----------|------|--------|---------|-----|-----|
| Frekuensi Begadang (kali/minggu) | 3.55 | 4.0 | 1.11 | 1 | 5 |
| Rasa Ngantuk saat Kuliah | 3.06 | 3.0 | 1.00 | 1 | 5 |
| Fokus Kuliah Setelah Begadang | 3.10 | 3.0 | 0.81 | 1 | 5 |
| Daya Ingat Materi | 2.82 | 3.0 | 0.67 | 1 | 4 |
| Pengaruh ke Ujian | 2.91 | 3.0 | 1.12 | 1 | 5 |
| Pengaruh ke Nilai Akademik | 2.99 | 3.0 | 1.11 | 1 | 5 |
| Penurunan Motivasi Belajar | 2.74 | 3.0 | 1.14 | 1 | 5 |

### Temuan Kunci

**Tujuan 1 — Pola Begadang (Mahasiswa ITSB Angkatan 25)**
-  **58.0%** (40 dari 69) mahasiswa Angkatan 25 hanya tidur **5–6 jam/malam** — jauh di bawah rekomendasi WHO (7–9 jam)
-  Mayoritas baru tidur pada pukul **00.00–01.00**
-  Rata-rata begadang **3.6x/minggu**

**Tujuan 2 — Dampak ke Konsentrasi**
-  **56.5%** responden mengalami **penurunan pemahaman materi** setelah begadang
-  Rasa ngantuk (**3.06/5**) adalah dampak paling konsisten yang dirasakan
-  Tidak ada variabel yang rata-ratanya melebihi 3.1 → dampak cenderung sedang

**Tujuan 3 — Faktor Penyebab**
-  **Tugas kuliah** = penyebab utama (**54 pilihan**)
-  **Hiburan** (medsos, game, film) = penyebab terbesar kedua

**Tujuan 4 — Kesadaran Mahasiswa**
-  **73.9%** tahu tidur ideal adalah 7–8 jam, namun realitanya mayoritas tidur 5–6 jam
-  **87.0%** ingin mengubah pola tidur, tapi sebagian besar merasa "ingin, tetapi sulit"

###  Uji Korelasi Spearman

| Variabel | r | p-value | Kekuatan | Signifikan? |
|----------|---|---------|----------|-------------|
| Rasa ngantuk di kelas | 0.114 | 0.3494 | Lemah | ✗ Tidak |
| Fokus kuliah | 0.173 | 0.1554 | Lemah | ✗ Tidak |
| Pengaruh ke nilai akademik | -0.120 | 0.3300 | Lemah | ✗ Tidak |
| Motivasi belajar turun | -0.111 | 0.3671 | Lemah | ✗ Tidak |
| Pengaruh ke ujian | 0.011 | 0.9295 | Lemah | ✗ Tidak |
| Daya ingat materi | -0.145 | 0.2394 | Lemah | ✗ Tidak |

> Semua nilai r < 0.3 dan p > 0.05 → **tidak ada korelasi yang signifikan secara statistik**. Kemungkinan penyebab: n=69 terlalu kecil untuk mendeteksi korelasi lemah.

---

##  Struktur File

```
 analisis-begadang-kelompok7/
├──  analisis_begadang_kelompok7.py          # Skrip analisis utama
├──  Sampling_survey__Jawaban__-_Form_Responses_1.csv  # Data mentah Google Forms
├──  viz1_pola_begadang.png                  # Grafik: durasi tidur & alasan begadang
├──  viz2_dampak_akademik.png                # Grafik: dampak begadang ke akademik
├──  viz3_korelasi_kesadaran.png             # Grafik: korelasi Spearman & kesadaran
└──  README.md
```

---

##  Visualisasi

| File | Isi |
|------|-----|
| `viz1_pola_begadang.png` | Distribusi durasi tidur per malam + alasan utama begadang |
| `viz2_dampak_akademik.png` | Rata-rata skor dampak begadang ke 6 variabel akademik (skala Likert 1–5) |
| `viz3_korelasi_kesadaran.png` | Koefisien korelasi Spearman + donut chart kesadaran mahasiswa |

---

##  Cara Menjalankan

### Prasyarat
Pastikan Python 3.x sudah terinstal, lalu install library berikut:

```bash
pip install pandas numpy matplotlib scipy
```

### Jalankan Analisis
```bash
python analisis_begadang_kelompok7.py
```

Output yang dihasilkan:
-  Ringkasan data di terminal (jumlah responden, statistik deskriptif, uji korelasi, kesimpulan)
-  3 file grafik PNG tersimpan di direktori yang sama

---

##  Library yang Digunakan

| Library | Fungsi |
|---------|--------|
| `pandas` | Membaca & mengolah data (DataFrame) |
| `numpy` | Hitung statistik (mean, std, dll.) |
| `matplotlib` | Membuat grafik & visualisasi |
| `scipy.stats` | Uji korelasi Spearman (statistik non-parametrik) |

---

##  Limitasi Penelitian

- **Cakupan sampel:** Penelitian ini hanya merepresentasikan **mahasiswa ITSB Angkatan 25**, bukan seluruh mahasiswa ITSB dari semua angkatan
- **Ukuran sampel:** n=69, di bawah target Slovin 91 (untuk populasi Angkatan 25) → **Margin of Error aktual ±11.8%**
- **Metode sampling:** Convenience sampling → **tidak representatif** seluruh mahasiswa ITSB Angkatan 25
- **Dominasi prodi:** S1 Sains Data **52.2%** dari total responden
- **Dominasi semester:** Semester 1–2 mencakup **91.3%** dari total responden — konsisten dengan target populasi Angkatan 25
- **Korelasi:** Tidak signifikan pada n=69 → perlu sampel lebih besar untuk konfirmasi

---

##  Tim Peneliti

**Kelompok 7** — S1 Sains Data ITSB  
Mata Kuliah: **Sampling dan Survei**

---

##  Catatan Metodologi

- Skala pengukuran: **Likert 1–5** untuk variabel ordinal
- Uji statistik: **Spearman Rank Correlation** (dipilih karena data ordinal, tidak mensyaratkan distribusi normal)
- Batas signifikansi: **p < 0.05** (standar ilmu sosial)
- Interpretasi kekuatan korelasi: |r| < 0.3 = Lemah | 0.3–0.5 = Sedang | >0.5 = Kuat
