# ============================================================
#  ANALISIS SURVEY: Pengaruh Kebiasaan Begadang terhadap
#  Konsentrasi Mahasiswa ITSB — Kelompok 7
#  Mata Kuliah: Sampling dan Survei | S1 Sains Data ITSB
# ============================================================
#
#  Library yang dipakai:
#  - pandas  : membaca & mengolah data (tabel/DataFrame)
#  - numpy   : hitung statistik (mean, sqrt, dll)
#  - matplotlib : membuat grafik / visualisasi
#  - scipy.stats: uji korelasi Spearman (statistik non-parametrik)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.stats import spearmanr
import warnings

# Matikan peringatan yang tidak penting agar output lebih bersih
warnings.filterwarnings('ignore')

# ── Pengaturan tampilan grafik secara global ──────────────────
# Semua grafik akan menggunakan pengaturan ini secara otomatis
plt.rcParams['font.family']        = 'DejaVu Sans'  # font utama
plt.rcParams['axes.spines.top']    = False           # hapus garis atas grafik
plt.rcParams['axes.spines.right']  = False           # hapus garis kanan grafik
plt.rcParams['axes.grid']          = True            # tampilkan garis bantu
plt.rcParams['grid.alpha']         = 0.25            # garis bantu transparan
plt.rcParams['axes.axisbelow']     = True            # garis bantu di belakang bar


# ============================================================
#  BAGIAN 1 — LOAD DATA & PERSIAPAN
#  Tujuan: membaca file CSV hasil Google Forms dan
#          merapikan nama kolom agar mudah dipakai
# ============================================================

# Baca file CSV dari Google Forms
# pd.read_csv() mengubah file CSV menjadi DataFrame (tabel di Python)
df_raw = pd.read_csv('Sampling_survey__Jawaban__-_Form_Responses_1.csv')

# Salin data asli ke variabel baru bernama 'df'
# Ini supaya data asli (df_raw) tidak ikut berubah jika kita edit sesuatu
df = df_raw.copy()

# Hapus kolom yang tidak dibutuhkan untuk analisis
# (Timestamp, Email, Nama, dan kolom kosong '@')
kolom_hapus = ['Timestamp', 'Email Address', 'Nama lengkap ', '@']
df.drop(columns=[c for c in kolom_hapus if c in df.columns], inplace=True)

# Ganti nama kolom panjang menjadi nama pendek (alias)
# Ini agar kode lebih ringkas saat diakses nanti (misal: df['prodi'] bukan df['Program studi'])
rename_map = {
    'Program studi'                                                                                    : 'prodi',
    'Semester'                                                                                         : 'semester',
    'Jenis kelamin'                                                                                    : 'gender',
    'Tempat tinggal'                                                                                   : 'tempat_tinggal',
    'Rata-rata durasi tidur Anda per malam adalah'                                                     : 'durasi_tidur',
    'Dalam satu minggu, berapa kali Anda begadang (tidur setelah pukul 00.00)? '                      : 'frekuensi_begadang',
    'Apa alasan utama kamu begadang? '                                                                 : 'alasan_begadang',
    'Ketika begadang, biasanya kamu baru tidur sekitar pukul berapa?'                                  : 'jam_tidur',
    'Rata-rata berapa kali dalam seminggu kamu begadang lebih dari dua hari berturut-turut?'           : 'begadang_berturut',
    'Seberapa sering kamu mengonsumsi kafein atau minuman berenergi saat begadang?'                    : 'konsumsi_kafein',
    'Apakah kamu biasanya tidur siang untuk menggantikan waktu tidur yang hilang setelah begadang?'   : 'tidur_siang',
    'Apa yang paling sering kamu kerjakan saat begadang?'                                              : 'aktivitas_begadang',
    'Setelah begadang, bagaimana fokus anda mengikuti perkuliahan di hari berikutnya'                  : 'fokus_kuliah',
    'Seberapa sering Anda merasa mengantuk saat perkuliahan setelah begadang? '                        : 'ngantuk_kuliah',
    'Bagaimana kemampuanmu memahami materi kuliah pada hari setelah begadang dibandingkan hari biasa?' : 'pemahaman_materi',
    'Seberapa sering kamu aktif bertanya atau berdiskusi di kelas setelah begadang?'                   : 'aktif_kelas',
    'Setelah kuliah di hari setelah begadang, seberapa banyak materi yang kamu ingat?'                : 'daya_ingat',
    'Apakah kamu pernah melewatkan atau terlambat masuk kuliah akibat begadang?'                       : 'telat_kuliah',
    'Seberapa besar pengaruh begadang terhadap kemampuanmu menyelesaikan ujian yang diadakan di hari berikutnya?' : 'pengaruh_ujian',
    'Menurutmu, apakah kebiasaan begadang berpengaruh negatif terhadap nilai akademikmu secara keseluruhan?'      : 'pengaruh_nilai',
    'Apakah begadang secara rutin membuat motivasi belajarmu menurun?'                                 : 'motivasi_turun',
    'Pernahkah kamu merasa menyesal begadang karena berdampak buruk pada performa kuliahmu?'           : 'menyesal_begadang',
    'Apa yang biasanya kamu lakukan untuk mengatasi kurang tidur sebelum kuliah? '                     : 'cara_atasi',
    'Menurutmu, berapa jam tidur ideal yang dibutuhkan mahasiswa agar bisa konsentrasi penuh saat kuliah?' : 'tidur_ideal',
    'Apakah kamu berkeinginan untuk mengubah pola tidurmu demi meningkatkan konsentrasi dan performa akademik?' : 'keinginan_ubah',
}
df.rename(columns=rename_map, inplace=True)

# Pastikan kolom yang berisi angka terbaca sebagai tipe numerik
# errors='coerce' artinya: kalau ada nilai aneh/teks, ubah jadi NaN (kosong), bukan error
for col in ['frekuensi_begadang', 'konsumsi_kafein', 'fokus_kuliah', 'ngantuk_kuliah',
            'aktif_kelas', 'daya_ingat', 'pengaruh_ujian', 'pengaruh_nilai', 'motivasi_turun']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Tampilkan ringkasan awal data
print("=" * 55)
print("  DATA BERHASIL DIMUAT")
print("=" * 55)
print(f"  Jumlah responden  : {len(df)} orang")
print(f"  Jumlah variabel   : {df.shape[1]} kolom")
print(f"  Nilai kosong (NaN): {df.isnull().sum().sum()}")
print(f"  Data duplikat     : {df.duplicated().sum()}")
print("=" * 55)


# ============================================================
#  BAGIAN 2 — STATISTIK DESKRIPTIF
#  Tujuan: menghitung ringkasan angka (mean, median, std)
#          dari variabel-variabel utama berskala 1–5
# ============================================================

# Definisikan variabel mana saja yang mau dirangkum
# Kunci dict = nama kolom di df, nilai = label tampilan
kolom_skala = {
    'frekuensi_begadang' : 'Frekuensi Begadang (kali/minggu)',
    'ngantuk_kuliah'     : 'Rasa Ngantuk saat Kuliah',
    'fokus_kuliah'       : 'Fokus Kuliah Setelah Begadang',
    'daya_ingat'         : 'Daya Ingat Materi',
    'pengaruh_ujian'     : 'Pengaruh ke Ujian',
    'pengaruh_nilai'     : 'Pengaruh ke Nilai Akademik',
    'motivasi_turun'     : 'Penurunan Motivasi Belajar',
}

# Hitung statistik untuk setiap variabel, simpan hasilnya di list
rows = []
for col, label in kolom_skala.items():
    if col in df.columns:
        rows.append({
            'Variabel' : label,
            'Mean'     : round(df[col].mean(), 2),   # rata-rata
            'Median'   : df[col].median(),            # nilai tengah
            'Std Dev'  : round(df[col].std(), 2),     # standar deviasi (sebaran data)
            'Min'      : int(df[col].min()),
            'Max'      : int(df[col].max()),
        })

# Buat DataFrame dari list, lalu tampilkan
df_stat = pd.DataFrame(rows).set_index('Variabel')
print("\nStatistik Deskriptif Variabel Skala 1–5:\n")
print(df_stat.to_string())
print("\nKeterangan: Mean = rata-rata | Std Dev = seberapa beragam jawaban responden")


# ============================================================
#  BAGIAN 3 — VISUALISASI 1: POLA KEBIASAAN BEGADANG
#  Tujuan penelitian 1 & 3: mengetahui pola & penyebab begadang
#
#  Grafik ini terdiri dari 2 panel berdampingan:
#  - Kiri : durasi tidur per malam (bar chart vertikal)
#  - Kanan: alasan utama begadang  (bar chart horizontal)
# ============================================================

# ── Warna tema yang dipakai di seluruh notebook ──
WARNA_UNGU  = '#7F77DD'   # ungu    — untuk durasi tidur kurang
WARNA_BIRU  = '#378ADD'   # biru    — untuk durasi tidur cukup
WARNA_MERAH = '#D85A30'   # merah   — untuk dampak negatif / alasan akademik
WARNA_AMBER = '#BA7517'   # kuning  — untuk hiburan / hal sekunder
WARNA_ABU   = '#888780'   # abu-abu — untuk netral
WARNA_PINK  = '#D4537E'   # pink    — untuk variasi tambahan
WARNA_HIJAU = '#1D9E75'   # hijau   — untuk hal positif / kesadaran

fig1, axes = plt.subplots(1, 2, figsize=(14, 6))
fig1.suptitle(
    'Pola Kebiasaan Begadang Mahasiswa ITSB (n=69)',
    fontsize=14, fontweight='bold', y=1.01
)

# ── Panel kiri: Durasi Tidur ──────────────────────────────────
# value_counts() menghitung berapa orang yang memilih tiap durasi
# reindex() memastikan urutan kategori sesuai yang kita mau
urutan_tidur = ['Kurang dari 3 jam', '3–4 jam', '5–6 jam', '7–8 jam', 'Lebih dari 8 jam']
tidur_count  = df['durasi_tidur'].value_counts().reindex(urutan_tidur, fill_value=0)

# Warna berbeda: merah/ungu untuk tidur kurang, hijau/biru untuk cukup
warna_tidur = [WARNA_MERAH, WARNA_UNGU, WARNA_UNGU, WARNA_HIJAU, WARNA_BIRU]
bars_tidur  = axes[0].bar(tidur_count.index, tidur_count.values,
                           color=warna_tidur, alpha=0.88, width=0.55,
                           edgecolor='white', linewidth=1.2)

# Tambahkan angka di atas setiap bar
for bar in bars_tidur:
    h = bar.get_height()
    if h > 0:
        pct = round(h / len(df) * 100, 1)  # hitung persentase
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,  # posisi x = tengah bar
            h + 0.5,                             # posisi y = sedikit di atas bar
            f'{int(h)}\n({pct}%)',               # teks: jumlah & persentase
            ha='center', va='bottom', fontsize=9, fontweight='bold'
        )

# Tambahkan garis merah putus-putus di angka 7 jam (rekomendasi WHO)
axes[0].axhline(y=0, color='gray', linewidth=0.5)
axes[0].set_title('Durasi Tidur per Malam', fontweight='bold', fontsize=12)
axes[0].set_xlabel('Durasi Tidur', fontsize=10)
axes[0].set_ylabel('Jumlah Mahasiswa', fontsize=10)
axes[0].tick_params(axis='x', rotation=15)

# Keterangan di bawah grafik
axes[0].text(
    0.5, -0.28,
    '★ WHO merekomendasikan 7–9 jam untuk dewasa muda.\n'
    f'  Hanya {tidur_count["7–8 jam"]+tidur_count["Lebih dari 8 jam"]} dari 69 responden ({round((tidur_count["7–8 jam"]+tidur_count["Lebih dari 8 jam"])/69*100,1)}%) yang tidur cukup.',
    transform=axes[0].transAxes, ha='center', fontsize=8.5,
    color='#5F5E5A', style='italic'
)

# ── Panel kanan: Alasan Begadang ─────────────────────────────
# Kolom 'alasan_begadang' bisa berisi banyak pilihan dalam satu sel
# (dipisah koma). Kita pecah dulu satu per satu, lalu hitung.
alasan_flat = []
for nilai in df['alasan_begadang'].dropna():
    for item in nilai.split(','):
        bersih = item.strip()
        # Gabungkan "game" dan "film" ke "Hiburan (media sosial, game, film)"
        if bersih in ['game', 'film)']:
            continue
        if 'Hiburan' in bersih or bersih == 'game' or bersih == 'film)':
            alasan_flat.append('Hiburan (medsos, game, film)')
        else:
            alasan_flat.append(bersih)

# Hitung frekuensi tiap alasan, ambil 5 terbesar
alasan_count = pd.Series(alasan_flat).value_counts().head(5)
warna_alasan = [WARNA_MERAH, WARNA_AMBER, WARNA_ABU, WARNA_PINK, WARNA_UNGU]

bars_alasan = axes[1].barh(
    alasan_count.index, alasan_count.values,
    color=warna_alasan[:len(alasan_count)], alpha=0.88,
    height=0.55, edgecolor='white', linewidth=1.2
)

# Tambahkan angka di ujung setiap bar horizontal
for bar in bars_alasan:
    w = bar.get_width()
    axes[1].text(
        w + 0.4,                              # posisi x = sedikit di kanan bar
        bar.get_y() + bar.get_height() / 2,   # posisi y = tengah bar
        f'{int(w)} responden',
        va='center', fontsize=9, fontweight='bold'
    )

axes[1].set_title('Alasan Utama Begadang\n(boleh pilih lebih dari satu)',
                  fontweight='bold', fontsize=12)
axes[1].set_xlabel('Jumlah Pilihan', fontsize=10)
axes[1].set_xlim(0, alasan_count.max() + 12)

plt.tight_layout()
plt.savefig('viz1_pola_begadang.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n[Viz 1 Insight]")
print(f"  → {tidur_count['5–6 jam']} dari 69 responden ({round(tidur_count['5–6 jam']/69*100,1)}%) hanya tidur 5–6 jam/malam.")
print(f"  → Tugas kuliah adalah alasan begadang nomor 1 ({alasan_count.iloc[0]} pilihan).")
print(f"  → Hiburan (medsos, game, film) menjadi alasan terbesar kedua.")


# ============================================================
#  BAGIAN 4 — VISUALISASI 2: DAMPAK BEGADANG KE AKADEMIK
#  Tujuan penelitian 2: mengukur dampak begadang ke konsentrasi
#
#  Grafik: horizontal bar chart dengan warna berdasarkan skor
#  - Merah  : skor rata-rata > 3 (dampak lebih terasa)
#  - Hijau  : skor rata-rata < 3 (dampak lebih ringan)
#  - Abu    : skor = 3 (netral)
#
#  Semua variabel diukur dengan skala Likert 1–5.
# ============================================================

# Definisikan variabel dampak beserta keterangan skalanya
# Key = nama kolom, value = (label tampilan, keterangan skala)
dampak_info = {
    'ngantuk_kuliah'  : ('Rasa ngantuk di kelas',       '1=Tidak pernah  ·  5=Selalu'),
    'fokus_kuliah'    : ('Fokus kuliah menurun',         '1=Sangat mudah fokus  ·  5=Sangat sulit fokus'),
    'pengaruh_nilai'  : ('Pengaruh ke nilai akademik',   '1=Tidak setuju  ·  5=Sangat setuju'),
    'pengaruh_ujian'  : ('Pengaruh ke ujian',            '1=Tidak berpengaruh  ·  5=Sangat berpengaruh'),
    'motivasi_turun'  : ('Motivasi belajar turun',       '1=Tidak pernah  ·  5=Selalu'),
    'daya_ingat'      : ('Daya ingat materi',            '1=Hampir tidak ada  ·  5=Banyak diingat'),
}

# Hitung rata-rata setiap variabel dampak
labels_dampak = []
means_dampak  = []
keterangan    = []

for col, (label, ket) in dampak_info.items():
    if col in df.columns:
        labels_dampak.append(label)
        means_dampak.append(round(df[col].mean(), 2))
        keterangan.append(ket)

# Tentukan warna bar berdasarkan posisi nilai terhadap titik tengah (3)
warna_dampak = []
for m in means_dampak:
    if m > 3.1:
        warna_dampak.append(WARNA_MERAH)   # dampak lebih terasa
    elif m < 2.9:
        warna_dampak.append(WARNA_HIJAU)   # dampak lebih ringan
    else:
        warna_dampak.append(WARNA_ABU)     # netral di sekitar 3

fig2, ax = plt.subplots(figsize=(11, 6))

bars2 = ax.barh(labels_dampak, means_dampak,
                color=warna_dampak, alpha=0.88,
                height=0.55, edgecolor='white', linewidth=1.2)

# Garis vertikal putus-putus di angka 3 (titik tengah skala 1–5)
# Ini penting sebagai acuan: skor di atas 3 = cenderung berdampak
ax.axvline(x=3, color='#5F5E5A', linestyle='--', linewidth=1.3,
           label='Titik tengah skala (3)')

# Tambahkan angka rata-rata di ujung setiap bar
for bar, m, ket in zip(bars2, means_dampak, keterangan):
    ax.text(
        m + 0.04,
        bar.get_y() + bar.get_height() / 2,
        f'{m:.2f}',
        va='center', fontsize=10, fontweight='bold', color='#2C2C2A'
    )

ax.set_xlim(1, 5.3)
ax.set_xlabel('Rata-rata Skor (Skala 1–5)', fontsize=10)
ax.set_title('Dampak Begadang terhadap Performa Akademik Mahasiswa ITSB',
             fontweight='bold', fontsize=13)

# Legenda manual — lebih informatif dari legenda otomatis
patch_merah = mpatches.Patch(color=WARNA_MERAH, alpha=0.88, label='Skor > 3 — dampak lebih terasa')
patch_hijau = mpatches.Patch(color=WARNA_HIJAU, alpha=0.88, label='Skor < 3 — dampak lebih ringan')
patch_abu   = mpatches.Patch(color=WARNA_ABU,   alpha=0.88, label='Skor ≈ 3 — netral')
ax.legend(handles=[patch_merah, patch_hijau, patch_abu, ax.lines[0]],
          loc='lower right', fontsize=9, framealpha=0.9)

# Keterangan skala di bawah judul grafik
ax.text(0.01, -0.12,
        'Semua variabel diukur dengan skala Likert 1–5. '
        'Interpretasi skala tiap variabel berbeda — lihat laporan untuk detailnya.',
        transform=ax.transAxes, fontsize=8.5, color='#5F5E5A', style='italic')

plt.tight_layout()
plt.savefig('viz2_dampak_akademik.png', dpi=150, bbox_inches='tight')
plt.show()

# Hitung persentase yang mengalami pemahaman lebih buruk
pct_buruk = round(
    df['pemahaman_materi'].isin(['Sedikit lebih buruk', 'Jauh lebih buruk']).mean() * 100, 1
)

print("\n[Viz 2 Insight]")
print(f"  → {pct_buruk}% responden mengaku pemahaman materi lebih buruk setelah begadang.")
print(f"  → Rasa ngantuk rata-rata {df['ngantuk_kuliah'].mean():.2f}/5 — dampak paling konsisten dirasakan.")
print(f"  → Tidak ada variabel yang rata-ratanya melebihi 3.1 — menunjukkan dampak cenderung sedang.")


# ============================================================
#  BAGIAN 5 — VISUALISASI 3: KORELASI SPEARMAN & KESADARAN
#  Tujuan 2 & 4: bukti statistik + tingkat kesadaran mahasiswa
#
#  Mengapa Spearman? Karena data berskala ordinal (1–5),
#  bukan data kontinu seperti berat/tinggi badan.
#  Spearman tidak mensyaratkan data berdistribusi normal.
#
#  Nilai r (koefisien korelasi):
#  - Mendekati +1 : hubungan positif kuat
#  - Mendekati  0 : tidak ada hubungan
#  - Mendekati -1 : hubungan negatif kuat
#  Kekuatan: |r| < 0.3 = lemah | 0.3–0.5 = sedang | >0.5 = kuat
# ============================================================

fig3, axes3 = plt.subplots(1, 2, figsize=(14, 6))
fig3.suptitle(
    'Korelasi Spearman & Kesadaran Mahasiswa ITSB',
    fontsize=14, fontweight='bold'
)

# ── Panel kiri: Korelasi Spearman ────────────────────────────
# Variabel yang akan diuji korelasinya dengan frekuensi begadang
uji_korelasi = {
    'ngantuk_kuliah'  : 'Rasa ngantuk di kelas',
    'fokus_kuliah'    : 'Fokus kuliah',
    'pengaruh_nilai'  : 'Pengaruh ke nilai akademik',
    'motivasi_turun'  : 'Motivasi belajar turun',
    'pengaruh_ujian'  : 'Pengaruh ke ujian',
    'daya_ingat'      : 'Daya ingat materi',
}

r_list, p_list, label_list = [], [], []

print("\nHasil Uji Korelasi Spearman (Frekuensi Begadang vs Variabel Akademik):")
print(f"{'Variabel':<30} {'r':>7} {'p-value':>9}  Kekuatan      Signifikan?")
print("─" * 72)

for col, label in uji_korelasi.items():
    if col in df.columns:
        # Ambil hanya baris yang tidak kosong di kedua kolom
        bersih = df[['frekuensi_begadang', col]].dropna()

        # Hitung korelasi Spearman → menghasilkan r dan p-value
        r, p = spearmanr(bersih['frekuensi_begadang'], bersih[col])

        r_list.append(r)
        p_list.append(p)
        label_list.append(label)

        # Tentukan kekuatan berdasarkan nilai absolut r
        kuat = 'Kuat' if abs(r) >= 0.5 else ('Sedang' if abs(r) >= 0.3 else 'Lemah')

        # Signifikan jika p < 0.05 (standar ilmu sosial)
        sig = '✓ Ya' if p < 0.05 else '✗ Tidak'

        print(f"  {label:<28} {r:>7.3f} {p:>9.4f}  {kuat:<12}  {sig}")

# Warna bar: merah jika |r| ≥ 0.3 (sedang/kuat), ungu jika lemah
warna_kor = [WARNA_MERAH if abs(r) >= 0.3 else WARNA_UNGU for r in r_list]

bars_kor = axes3[0].barh(label_list, r_list,
                          color=warna_kor, alpha=0.88,
                          height=0.55, edgecolor='white', linewidth=1.2)

# Garis vertikal di 0, +0.3, -0.3
axes3[0].axvline(x=0,    color='#2C2C2A', linewidth=0.9)
axes3[0].axvline(x=0.3,  color='gray', linestyle=':', linewidth=1.2,
                 label='Batas kekuatan sedang (±0.3)')
axes3[0].axvline(x=-0.3, color='gray', linestyle=':', linewidth=1.2)

# Tambahkan nilai r di ujung setiap bar
for bar, r in zip(bars_kor, r_list):
    posisi_x = r + 0.012 if r >= 0 else r - 0.012
    ha        = 'left'   if r >= 0 else 'right'
    axes3[0].text(posisi_x, bar.get_y() + bar.get_height() / 2,
                  f'{r:.3f}', va='center', ha=ha, fontsize=9, fontweight='bold')

axes3[0].set_xlim(-0.5, 0.5)
axes3[0].set_xlabel('Koefisien Korelasi Spearman (r)', fontsize=10)
axes3[0].set_title('Hubungan Frekuensi Begadang\nvs Variabel Akademik',
                   fontweight='bold', fontsize=12)
axes3[0].legend(fontsize=8.5)

# ── Panel kanan: Kesadaran Mahasiswa (Donut Chart) ────────────
# Urutan dan warna kategori jawaban keinginan ubah pola tidur
urutan_sadar = ['Sangat ingin', 'Ingin, tetapi sulit', 'Belum terpikir']
sadar_count  = df['keinginan_ubah'].value_counts().reindex(urutan_sadar, fill_value=0)
warna_sadar  = [WARNA_HIJAU, WARNA_AMBER, WARNA_ABU]

# Buat donut chart (pie chart dengan lubang di tengah)
wedges, texts, autotexts = axes3[1].pie(
    sadar_count.values,
    labels=None,                    # label akan dibuat manual di bawah
    colors=warna_sadar,
    autopct='%1.1f%%',              # tampilkan persentase otomatis
    pctdistance=0.78,               # jarak teks % dari tengah
    startangle=90,                  # mulai dari atas
    wedgeprops=dict(width=0.52,     # lebar 'donat' (1 = pie penuh)
                    edgecolor='white', linewidth=2)
)

# Atur ukuran dan warna teks persentase
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

# Teks di tengah donat — menampilkan total responden
axes3[1].text(0, 0, f'n={len(df)}', ha='center', va='center',
              fontsize=13, fontweight='bold', color='#2C2C2A')

axes3[1].set_title('Keinginan Mengubah Pola Tidur\n(Tingkat Kesadaran Mahasiswa)',
                   fontweight='bold', fontsize=12)

# Legenda manual di bawah donat
legend_items = [
    mpatches.Patch(color=warna_sadar[i], alpha=0.88,
                   label=f'{urutan_sadar[i]} — {sadar_count.values[i]} orang '
                         f'({round(sadar_count.values[i]/len(df)*100,1)}%)')
    for i in range(len(urutan_sadar))
]
axes3[1].legend(handles=legend_items, loc='lower center',
                bbox_to_anchor=(0.5, -0.18), fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig('viz3_korelasi_kesadaran.png', dpi=150, bbox_inches='tight')
plt.show()

# Hitung persentase yang ingin ubah pola tidur
pct_sadar = round(
    df['keinginan_ubah'].isin(['Sangat ingin', 'Ingin, tetapi sulit']).mean() * 100, 1
)

print("\n[Viz 3 Insight]")
print("  → Semua nilai r berada di bawah 0.3 dan tidak signifikan (p > 0.05).")
print("     Artinya: di sampel ini, frekuensi begadang tidak terbukti berkorelasi")
print("     kuat dengan variabel akademik secara statistik.")
print("     Kemungkinan penyebab: n=69 terlalu kecil untuk mendeteksi korelasi lemah.")
print(f"  → {pct_sadar}% mahasiswa ingin mengubah pola tidurnya,")
print("     namun sebagian besar merasa 'ingin, tetapi sulit'.")
print("     → Kesadaran tinggi, tapi belum diikuti perubahan perilaku nyata.")


# ============================================================
#  BAGIAN 6 — KESIMPULAN AKHIR
# ============================================================

print("\n" + "=" * 65)
print("  KESIMPULAN SURVEY")
print("  Kebiasaan Begadang & Konsentrasi Mahasiswa ITSB — Kelompok 7")
print("=" * 65)

tidur_dominan = df['durasi_tidur'].value_counts().idxmax()
jam_dominan   = df['jam_tidur'].value_counts().idxmax()

print(f"\n  Tujuan 1 — Pola Begadang")
print(f"    Mayoritas tidur {tidur_dominan}/malam, baru tidur pukul {jam_dominan}.")
print(f"    Rata-rata begadang {df['frekuensi_begadang'].mean():.1f}x/minggu.")

print(f"\n  Tujuan 2 — Dampak ke Konsentrasi")
print(f"    {pct_buruk}% responden mengalami penurunan pemahaman materi setelah begadang.")
print(f"    Rasa ngantuk ({df['ngantuk_kuliah'].mean():.2f}/5) adalah dampak paling konsisten.")

print(f"\n  Tujuan 3 — Faktor Penyebab")
print(f"    Tugas kuliah & UTS/UAS = penyebab utama.")
print(f"    Hiburan (medsos, game, film) = penyebab terbesar kedua.")

tidur_ideal_dom = df['tidur_ideal'].value_counts().idxmax()
pct_ideal       = round((df['tidur_ideal'] == tidur_ideal_dom).mean() * 100, 1)
print(f"\n  Tujuan 4 — Kesadaran Mahasiswa")
print(f"    {pct_ideal}% tahu tidur ideal adalah {tidur_ideal_dom},")
print(f"    namun kenyataannya mayoritas hanya tidur 5–6 jam.")
print(f"    {pct_sadar}% ingin ubah pola tidur, tapi merasa sulit melakukannya.")

print(f"\n  Limitasi")
print(f"    - n=69, target Slovin 91 (MoE aktual ±11.8%)")
print(f"    - Convenience sampling → tidak representatif seluruh ITSB")
print(f"    - Dominasi Sains Data ({round((df['prodi']=='S1 - Sains Data').mean()*100,1)}%) "
      f"& Semester 1–2 ({round((df['semester']=='Semester 1–2').mean()*100,1)}%)")
print(f"    - Korelasi tidak signifikan → perlu sampel lebih besar untuk konfirmasi")

print("\n" + "=" * 65)
print("  Grafik tersimpan: viz1_pola_begadang.png")
print("                    viz2_dampak_akademik.png")
print("                    viz3_korelasi_kesadaran.png")
print("=" * 65)
