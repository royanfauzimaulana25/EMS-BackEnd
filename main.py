from fastapi import FastAPI, File, Form, UploadFile, Body
import Utils as utils
from pydantic import BaseModel
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
# from weasyprint import HTML
# import Test as test 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth

@app.post("/register")
async def registration(
    username : str = Form(...),
    password : str = Form(...)
    ) :

    response = utils.add_account(username, password, 'Peserta')

    return response
    
@app.post("/login")
async def login(
    username : str = Form(...),
    password : str = Form(...)
    ) :
    
    response = utils.login_verification(username, password)    

    return response

# Registration ===================================================================

## Photography
@app.post("/photography/")
async def add_photography(
    id_user: Annotated[str, Form()],
    asal_sekolah: Annotated[str, Form()],
    surat_tugas : Annotated[UploadFile, File()],
    no_telepon : Annotated[str, Form()],
    nama_lengkap : Annotated[str, Form()],
    jenis_kelamin : Annotated[str, Form()],
    alamat : Annotated[str, Form()],
    pas_photo : Annotated[UploadFile, File()],
    kartu_pelajar : Annotated[UploadFile, File()]
    ) :
    
    info = {        
        "id_user": id_user, 
        "nama" : nama_lengkap,
        "jenis_kelamin" : jenis_kelamin,
        "alamat" : alamat,
        "pas_photo" : pas_photo,
        "kartu_pelajar" : kartu_pelajar,
        "id_lomba" : "110",
        "npsn" : asal_sekolah,
        "surat_tugas" : surat_tugas,
        "no_telp" : no_telepon
            }
    
    response = utils.photography(info)

    return response

# Get Data
@app.get("/photography/")
async def get_photography(id_user) :
    
    response = utils.get_photography_data(id_user)

    return response


## Basketball  
@app.post("/basketball/")
async def add_basketball(
    id_user: Annotated[str, Form()],
    asal_sekolah: Annotated[str, Form()],
    surat_tugas : Annotated[UploadFile, File()],
    no_telepon : Annotated[str, Form()],
    nama_tim : Annotated[str, Form()],
    kategori_tim : Annotated[str, Form()],
    nama_pelatih : Annotated[str, Form()],
    nama_official : Annotated[str, Form()],

    nama_lengkap : Annotated[str, Form()],
    jenis_kelamin : Annotated[str, Form()],
    alamat : Annotated[str, Form()],
    no_punggung : Annotated[str, Form()],
    pas_photo : Annotated[UploadFile, File()],
    kartu_pelajar : Annotated[UploadFile, File()],

    nama_lengkap_1 : Annotated[str, Form()],
    jenis_kelamin_1 : Annotated[str, Form()],
    alamat_1 : Annotated[str, Form()],
    no_punggung_1 : Annotated[str, Form()],
    pas_photo_1 : Annotated[UploadFile, File()],
    kartu_pelajar_1 : Annotated[UploadFile, File()],

    nama_lengkap_2 : Annotated[str, Form()],
    jenis_kelamin_2 : Annotated[str, Form()],
    alamat_2 : Annotated[str, Form()],
    no_punggung_2 : Annotated[str, Form()],
    pas_photo_2 : Annotated[UploadFile, File()],
    kartu_pelajar_2 : Annotated[UploadFile, File()],

    nama_lengkap_3 : Annotated[str, Form()],
    jenis_kelamin_3 : Annotated[str, Form()],
    alamat_3 : Annotated[str, Form()],
    no_punggung_3 : Annotated[str, Form()],
    pas_photo_3 : Annotated[UploadFile, File()],
    kartu_pelajar_3 : Annotated[UploadFile, File()]
    ) :
    
    info = {        
        "uuid": id_user, 
        "id_lomba" : "150",
        "npsn" : asal_sekolah,
        "surat_tugas" : surat_tugas,
        "no_telp" : no_telepon,
        "nama_tim" : nama_tim,
        "kategori_tim" : kategori_tim,
        "nama_pelatih" : nama_pelatih,
        "nama_official" : nama_official,

        "nama" : nama_lengkap,
        "jenis_kelamin" : jenis_kelamin,
        "alamat" : alamat,
        "no_punggung" : no_punggung,
        "pas_photo" : pas_photo,
        "kartu_pelajar" : kartu_pelajar,
        "is_captain" : True,

        "nama_1" : nama_lengkap_1,
        "jenis_kelamin_1" : jenis_kelamin_1,
        "alamat_1" : alamat_1,
        "no_punggung_1" : no_punggung_1,
        "pas_photo_1" : pas_photo_1,
        "kartu_pelajar_1" : kartu_pelajar_1,
        "is_captain_1" : False,

        "nama_2" : nama_lengkap_2,
        "jenis_kelamin_2" : jenis_kelamin_2,
        "alamat_2" : alamat_2,
        "no_punggung_2" : no_punggung_2,
        "pas_photo_2" : pas_photo_2,
        "kartu_pelajar_2" : kartu_pelajar_2,
        "is_captain_2" : False,

        "nama_3" : nama_lengkap_3,
        "jenis_kelamin_3" : jenis_kelamin_3,
        "alamat_3" : alamat_3,
        "no_punggung_3" : no_punggung_3,
        "pas_photo_3" : pas_photo_3,
        "kartu_pelajar_3" : kartu_pelajar_3,
        "is_captain_3" : False
            }
    
    response = utils.basketball(info)

    return response

# Payment
class Info(BaseModel):
  id_bayar: str
  uuid: str
  metode_pembayaran: str
  jumlah_bayar: int

@app.post("/pay/")
async def pay(info : Info = Body(...)) :
    info =  {"id_bayar": info.id_bayar, 
             "uuid": info.uuid,   
             "metode_pembayaran": info.metode_pembayaran, 
             "jumlah_bayar": info.jumlah_bayar
             }
    response = utils.payBill(info)
    
    return response

# Get Data
@app.get("/basketball/")
async def get_basketball(id_user) :
    
    response = utils.get_basketball_data(id_user)

    return response

# Metadata
@app.get("/jenjang/")
async def get_jenjang() :
    
    response = utils.get_jenjang_data()

    return response

@app.get("/sekolah/")
async def get_sekolah(id) :
    
    response = utils.get_sekolah_data(id)

    return response

@app.get("/lomba/")
async def get_lomba(id) :
    
    response = utils.get_lomba_data(id)

    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(8000))