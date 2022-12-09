from app.model import OrderSchema

import requests

class URLrey():
    def getReyHarga(self,jalanAwal, kotaAwal, namaPelanggan,  jalanTujuan, kotaTujuan,):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            f'alamatAwal': {
                'nama': 'David N',
                'jalan': jalanAwal,
                'kota': kotaAwal,
            },
            f'alamatTujuan': {
                'nama': namaPelanggan,
                'jalan': jalanTujuan,
                'kota': kotaTujuan,
            },
        }

        response = requests.post('http://128.199.149.182/shoetify/order-shoetify', headers=headers, json=json_data)
        if response.status_code == 200:
            return response
        else:
            return {"Message": "Gagal mendapatkan data",
                    "response": response
            }