import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
from termcolor import colored
import pandas as pd
import matplotlib.pyplot as plt

def scrape_website(url, element, class_name, element_id, output_file, columns):
    try:
        # Menggunakan user-agent palsu
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        # Mengirim permintaan HTTP ke URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil

        # Parsing konten HTML menggunakan lxml
        soup = BeautifulSoup(response.content, 'lxml')

        # Mencari elemen, class, dan id yang diberikan oleh pengguna
        if class_name and element_id:
            target_elements = soup.find_all(element, {'class': class_name, 'id': element_id})
        elif class_name:
            target_elements = soup.find_all(element, {'class': class_name})
        elif element_id:
            target_elements = soup.find_all(element, {'id': element_id})
        else:
            target_elements = soup.find_all(element)

        if target_elements:
            # Menyimpan hasil ke dalam file CSV
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columns)

                for item in target_elements:
                    data = [item.find(col).text.strip() if item.find(col) else 'N/A' for col in columns]
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
            print(colored(f"Elemen '{element}' dengan class '{class_name}' dan id '{element_id}' tidak ditemukan di halaman.", 'red'))

    except requests.exceptions.RequestException as e:
        print(colored(f"Terjadi kesalahan: {e}", 'red'))

    # Menambahkan watermark
    print(colored("\nBy Firzi Fathir Mas'ud", 'cyan', attrs=['bold', 'underline']))

# Contoh penggunaan
url = input(colored("Masukkan URL: ", 'cyan'))
element = input(colored("Masukkan elemen target (misalnya: 'div', 'table', 'p', dll.): ", 'cyan'))
class_name = input(colored("Masukkan nama class elemen (kosongkan jika tidak ada): ", 'cyan'))
element_id = input(colored("Masukkan id elemen (kosongkan jika tidak ada): ", 'cyan'))
output_file = input(colored("Masukkan nama file output (misalnya: hasil_scraping.csv): ", 'cyan'))
columns = input(colored("Masukkan nama kolom yang ingin diambil (misalnya: 'h2, span, a'): ", 'cyan')).split(', ')
scrape_website(url, element, class_name, element_id, output_file, columns)