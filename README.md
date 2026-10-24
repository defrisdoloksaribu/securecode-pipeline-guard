\# SecureCode Pipeline Guard



\*\*Automated DevSecOps Security Pipeline for Python Applications\*\*



SecureCode Pipeline Guard adalah proyek automasi security testing yang mengintegrasikan berbagai security tools ke dalam CI/CD pipeline menggunakan GitHub Actions. Proyek ini dirancang untuk mendeteksi potensi kerentanan pada source code, dependency packages, dan secret yang tidak sengaja terunggah ke repository.



Project ini menerapkan prinsip \*\*Shift-Left Security\*\*, yaitu melakukan pemeriksaan keamanan sejak tahap awal development agar masalah dapat ditemukan sebelum perubahan dilanjutkan ke tahap berikutnya.



\## Project Overview



SecureCode Pipeline Guard mengotomatisasi beberapa security checks setiap kali ada perubahan kode melalui `push` atau `pull request`. Pipeline menjalankan unit tests, melakukan source code scanning, memeriksa dependency vulnerabilities, dan mendeteksi kemungkinan secret yang terekspos.



Proyek ini juga memiliki custom \*\*Security Gate\*\* yang mengevaluasi laporan hasil scanning dan menentukan apakah temuan keamanan tertentu harus memblokir proses pipeline.



\## Key Features



\- \*\*Automated Security Scanning:\*\* menjalankan security checks secara otomatis melalui GitHub Actions.

\- \*\*Static Application Security Testing (SAST):\*\* mendeteksi potensi masalah keamanan pada kode Python menggunakan Bandit.

\- \*\*Software Composition Analysis (SCA):\*\* memeriksa dependency packages terhadap database kerentanan yang diketahui menggunakan pip-audit.

\- \*\*Secret Detection:\*\* mendeteksi kemungkinan API keys, tokens, passwords, atau secret lainnya menggunakan Gitleaks.

\- \*\*Custom Security Gate:\*\* memblokir laporan yang mengandung temuan berlevel `HIGH` atau `CRITICAL`.

\- \*\*Unit Testing:\*\* menguji perilaku Security Gate menggunakan Python `unittest`.



\## Security Tools



| Tool | Purpose |

|---|---|

| GitHub Actions | Menjalankan automated CI security workflow |

| Bandit | Static Application Security Testing (SAST) untuk Python |

| pip-audit | Dependency vulnerability scanning |

| Gitleaks | Secret detection |

| Python unittest | Menguji logic pada Security Gate |



\## Pipeline Architecture



Alur kerja security pipeline:



1\. \*\*Code Push / Pull Request\*\* — developer mengirim perubahan ke repository.

2\. \*\*CI Initialization\*\* — GitHub Actions menyiapkan environment Python dan menginstal security tools.

3\. \*\*Unit Testing\*\* — automated tests dijalankan untuk memvalidasi fungsi aplikasi dan Security Gate.

4\. \*\*SAST Scanning\*\* — Bandit memindai source code Python dan menghasilkan laporan JSON.

5\. \*\*Security Gate Evaluation\*\* — laporan Bandit dievaluasi. Temuan `HIGH` atau `CRITICAL` menyebabkan pemeriksaan ini gagal.

6\. \*\*Dependency Scanning\*\* — pip-audit memeriksa dependency packages yang tercantum dalam `requirements-dev.txt`.

7\. \*\*Secret Scanning\*\* — Gitleaks memindai kemungkinan secret yang terekspos.

8\. \*\*Pipeline Result\*\* — GitHub Actions menampilkan status setiap job dan step agar hasil pemeriksaan dapat ditinjau.



\## Security Gate Logic



Custom Security Gate membaca laporan JSON dari security scanner dan menentukan hasil berdasarkan severity.



| Severity | Behavior |

|---|---|

| `LOW` | Pass |

| `MEDIUM` | Pass |

| `HIGH` | Fail |

| `CRITICAL` | Fail |

| Report missing or invalid | Fail with error |



Security Gate menggunakan exit codes agar kegagalan dapat dikenali oleh CI pipeline:



\- `0` — pemeriksaan berhasil.

\- `1` — ditemukan temuan yang memblokir.

\- `2` — laporan tidak tersedia, tidak valid, atau tidak dapat dibaca.



\*\*Note:\*\* Kebijakan ini merupakan aturan yang dikonfigurasi dalam proyek, bukan standar universal bahwa semua temuan `LOW` atau `MEDIUM` selalu aman.



\## Project Structure



```text

securecode-pipeline-guard/

├── .github/

│   └── workflows/

│       └── security.yml

├── app/

│   ├── main.py

│   └── security\_gate.py

├── tests/

│   └── test\_security\_gate.py

├── reports/                 # Local reports, excluded from Git

├── tools/                   # Local tools, excluded from Git

├── .gitignore

├── LICENSE

├── README.md

└── requirements-dev.txt

```



Folder `.venv/`, `reports/`, dan `tools/` digunakan untuk kebutuhan lokal dan dikecualikan dari version control sesuai konfigurasi `.gitignore`.



\## Getting Started



\### Prerequisites



Pastikan sudah tersedia:



\- Python 3.12 atau versi kompatibel dengan project.

\- Git.

\- Gitleaks binary jika ingin menjalankan secret scanning secara lokal.

\- Internet connection untuk menginstal security tools dan memeriksa database kerentanan.



\### 1. Clone Repository



```bash

git clone https://github.com/defrisdoloksaribu/securecode-pipeline-guard.git

cd securecode-pipeline-guard

```



\### 2. Create Virtual Environment



Windows:



```cmd

python -m venv .venv

.venv\\Scripts\\activate

```



\### 3. Install Development Dependencies



```bash

python -m pip install -r requirements-dev.txt

```



\### 4. Run Unit Tests



```bash

python -m unittest discover -s tests -v

```



\### 5. Run Bandit SAST Scan



```bash

bandit -r app -ll

```



Untuk menghasilkan laporan JSON yang dapat diproses oleh Security Gate:



```cmd

if not exist reports mkdir reports

bandit -r app -f json -o reports\\bandit-report.json

```



Jika Bandit melaporkan temuan, exit code-nya dapat menjadi nonzero. Periksa laporan yang dihasilkan sebelum menyimpulkan apakah temuan tersebut benar-benar berbahaya.



\### 6. Run Security Gate



```cmd

python app\\security\_gate.py reports\\bandit-report.json

```



Jika tidak ada temuan `HIGH` atau `CRITICAL`, hasil yang diharapkan:



```text

SECURITY GATE: PASSED

```



Jika laporan mengandung temuan yang memblokir:



```text

SECURITY GATE: FAILED

```



\### 7. Run Dependency Audit



```bash

pip-audit -r requirements-dev.txt

```



Perintah ini mengaudit dependency packages yang tercantum dalam `requirements-dev.txt`, termasuk tools pengembangan beserta dependensi transitive-nya. File ini bukan daftar runtime dependencies aplikasi; aplikasi saat ini menggunakan modul bawaan Python.



\### 8. Run Gitleaks Locally



Gunakan Gitleaks yang telah tersedia pada komputer:



```cmd

tools\\gitleaks.exe dir app

```



Sesuaikan path jika binary Gitleaks disimpan di lokasi berbeda. Untuk pemindaian riwayat Git, gunakan perintah dan konfigurasi Gitleaks yang sesuai dengan versi yang terpasang.



\## Validation and Test Results



Selama pengembangan, pemeriksaan berikut telah berhasil dijalankan:



\- \*\*Unit tests:\*\* 4 automated tests passed.

\- \*\*Bandit:\*\* tidak menemukan masalah pada kode aplikasi yang dipindai dalam pengujian tersebut.

\- \*\*pip-audit:\*\* tidak menemukan kerentanan yang diketahui pada dependency set yang diperiksa.

\- \*\*Gitleaks:\*\* tidak menemukan secret pada direktori `app/` yang dipindai.

\- \*\*GitHub Actions:\*\* empat workflow runs yang dilaporkan berhasil.

\- \*\*Security Gate negative test:\*\* laporan simulasi dengan severity `HIGH` menghasilkan `SECURITY GATE: FAILED`, sesuai dengan kebijakan yang dikonfigurasi.



Hasil ini menunjukkan bahwa komponen utama pipeline telah diuji. Namun, hasil scanning hanya berlaku untuk kode, dependencies, dan cakupan pemeriksaan pada saat pengujian. Hasil tersebut tidak menjamin seluruh sistem bebas dari kerentanan.



\## DevSecOps Concepts Demonstrated



Project ini menunjukkan penerapan beberapa konsep DevSecOps:



\- \*\*Shift-Left Security:\*\* security checks dilakukan sejak awal development.

\- \*\*CI/CD Automation:\*\* pemeriksaan berjalan otomatis pada event repository.

\- \*\*SAST:\*\* pemeriksaan statis terhadap source code.

\- \*\*SCA:\*\* pemeriksaan dependency vulnerabilities.

\- \*\*Secret Management Awareness:\*\* mencegah kredensial sensitif terunggah ke repository.

\- \*\*Policy-Based Security Gate:\*\* menerapkan aturan severity untuk menentukan kelulusan pemeriksaan.

\- \*\*Automated Testing:\*\* memvalidasi perilaku Security Gate melalui unit tests.



\## Future Improvements



Beberapa pengembangan yang dapat ditambahkan:



\- Mengunggah security reports sebagai GitHub Actions artifacts.

\- Menambahkan dependency pinning dan reproducible builds.

\- Mengintegrasikan container image scanning jika aplikasi dikemas menggunakan Docker.

\- Menambahkan branch protection dan required status checks.

\- Memperluas automated tests untuk malformed reports, missing reports, dan format scanner yang tidak valid.

\- Menambahkan notifikasi ketika pipeline gagal.



\## Disclaimer



SecureCode Pipeline Guard merupakan educational project untuk mempelajari implementasi DevSecOps dan automated security testing. Hasil scanner perlu ditinjau untuk mengonfirmasi temuan, dan proyek ini tidak menggantikan comprehensive security assessment.



\## Author



\*\*Defris Doloksaribu\*\*



GitHub: \[@defrisdoloksaribu](https://github.com/defrisdoloksaribu)



Repository: \[securecode-pipeline-guard](https://github.com/defrisdoloksaribu/securecode-pipeline-guard)



