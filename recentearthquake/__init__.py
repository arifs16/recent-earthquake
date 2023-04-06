import requests
import bs4

class RecentEarthquake:
    def __init__(self, url):
        self.description = 'To get the recent earthquake in Indonesia from BMKG.go.id'
        self.result = None
        self.url = url

    def ekstraksi_data(self):

        try:
            content = requests.get(self.url)
        except Exception:
            return None
        if content.status_code == 200:
            soup = bs4.BeautifulSoup(content.text, 'html.parser') #INSTANTIATION = INSTANTIASI = PENCIPTAAN OBJECT DARI CLASS

            result = soup.find('span', {'class': 'waktu'})
            result = result.text.split(', ')
            tanggal = result[0]
            waktu = result[1]

            result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
            result = result.findChildren('li')
            i = 0
            magnitudo = None
            kedalaman = None
            ls = None
            bt = None
            lokasi = None
            dirasakan = None

            for res in result:
                if i == 1:
                    magnitudo =  res.text
                elif i == 2:
                    kedalaman = res.text
                elif i == 3:
                    koordinat = res.text.split(' - ')
                    ls = koordinat[0]
                    bt = koordinat[1]
                elif i == 4:
                    lokasi = res.text
                elif i == 5:
                    dirasakan = res.text
                i = i + 1

            hasil = dict()
            hasil['tanggal'] = tanggal
            hasil['waktu'] = waktu
            hasil['magnitudo'] = magnitudo
            hasil['kedalaman'] = kedalaman
            hasil['koordinat'] = {'ls': ls, 'bt': bt}
            hasil['lokasi'] = lokasi
            hasil['dirasakan'] = dirasakan
            self.result = hasil
        else:
            return None


    def tampilkan_data(self):
        if self.result is None:
            print('Tidak bisa menemukan data gempa terkini')
            return

        print('The last earthquake based on BMKG')
        print(f"Date {self.result['tanggal']}")
        print(f"Time {self.result['waktu']}")
        print(f"Magnitude {self.result['magnitudo']}")
        print(f"Depth {self.result['kedalaman']}")
        print(f"Coordinate: {self.result['koordinat']['ls']}, {self.result['koordinat']['bt']}")
        print(f"Location {self.result['lokasi']}")
        print(f"{self.result['dirasakan']}")

    def run(self):
        self.ekstraksi_data()
        self.tampilkan_data()

if __name__ == '__main__':
    earthquake_in_indonesia = RecentEarthquake('https://bmkg.go.id')
    print('Package description', earthquake_in_indonesia.description)
    earthquake_in_indonesia.run()
    # earthquake_in_indonesia.ekstraksi_data()
    # earthquake_in_indonesia.tampilkan_data()
