from pydantic import BaseModel

class User(BaseModel):
    username: str
    name:str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInformation:
    username: str
    name: str
    coins: int
class OrderSchema(BaseModel):
    id: int
    nama: str
    alamat: str
    sepatu: str
    paket: str

    class Config:
        schema_extra = {
            "example": {
                "id" : 1,
                "nama" : "Peter Griffin",
                "alamat" : "Jalan Cisitu Elok No.7",
                "sepatu" : "Nike Court Vision Low",
                "paket" : "Reguler"
            }
        }