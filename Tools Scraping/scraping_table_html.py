import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
from termcolor import colored
import pandas as pd
import matplotlib.pyplot as plt

def scrape_website(url, table_class, output_file, columns):
    try:
        # Menggunakan user-agent palsu
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        # Mengirim permintaan HTTP ke URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil

        # Parsing konten HTML menggunakan html.parser
        soup = BeautifulSoup(response.content, 'html.parser')

        # Mencari elemen tabel yang diberikan oleh pengguna
        table = soup.find('table', {'class': table_class})
        if table:
            rows = table.find_all('tr')

            # Menyimpan hasil ke dalam file CSV
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columns)

                for row in rows[1:]:  # Melewati header
                    cols = row.find_all('td')
                    data = [col.text.strip() if col else 'N/A' for col in cols]
                    writer.writerow(data)

            print(colored(f"Hasil scraping telah disimpan dalam file {output_file}", 'green'))

            # Membaca file CSV dan menambahkan data statistik
            df = pd.read_csv(output_file)
            stats = df.describe(include='all')
            stats.to_csv(output_file, mode='a')

            print(colored("Data statistik telah ditambahkan ke dalam file", 'green'))

            # Memeriksa missing values
            missing_values = df.isnull().sum()
            print(colored("Missing values dalam data:", 'yellow'))
            print(missing_values)

            # Membuat bagan dan menyimpannya sebagai gambar
            plt.figure(figsize=(10, 6))
            df.plot(kind='bar')
            plt.title('Data Scraping Result')
            plt.xlabel('Index')
            plt.ylabel('Values')
            plt.savefig('chart.png')
            print(colored("Bagan telah dibuat dan disimpan sebagai 'chart.png'", 'green'))
        else:
            print(colored(f"Tabel dengan kelas '{table_class}' tidak ditemukan di halaman.", 'red'))

    except requests.exceptions.RequestException as e:
        print(colored(f"Terjadi kesalahan: {e}", 'red'))

    # Menambahkan watermark
    print(colored("\nBy Firzi Fathir Mas'ud", 'cyan', attrs=['bold', 'underline']))

# Contoh penggunaan
url = input(colored("Masukkan URL: ", 'cyan'))
table_class = input(colored("Masukkan kelas tabel: ", 'cyan'))
output_file = input(colored("Masukkan nama file output (misalnya: hasil_scraping.csv): ", 'cyan'))
columns = input(colored("Masukkan nama kolom yang ingin diambil (misalnya: 'Kolom1, Kolom2, Kolom3'): ", 'cyan')).split(', ')
scrape_website(url, table_class, output_file, columns)