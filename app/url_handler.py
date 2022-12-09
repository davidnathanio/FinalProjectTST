from app.model import OrderSchema

import requests

class URLrey():
    def getReyHarga(self, jalanAwal, kotaAwal, jalanTujuan, kotaTujuan,):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            f'alamatAwal': {
                'jalan': jalanAwal,
                'kota': kotaAwal,
            },
            f'alamatTujuan': {
                'jalan': jalanTujuan,
                'kota': kotaTujuan,
            },
        }

        response = requests.post('http://128.199.149.182/shoetify/order-shoetify', headers=headers, json=json_data)
        return response