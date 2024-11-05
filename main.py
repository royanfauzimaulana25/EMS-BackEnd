from fastapi import FastAPI, File, Form, UploadFile, Body
import Utils as utils
from pydantic import BaseModel
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth
@app.get("/register/status")
async def registerStatus(iduser) :
    
    response = utils.register_status(iduser)    

    return response

@app.post("/register")
async def registration(
    username : str = Form(...),
    password : str = Form(...)
    ) :

    response = utils.add_account(username, password, 'Peserta')

    return response

@app.post("/register/pj")
async def registration(
    username : str = Form(...),
    password : str = Form(...),
    nama : str = Form(...),
    jenis_kelamin : str = Form(...),
    lomba : str = Form(...)
    ) :

    response = utils.add_account_pj(username, password, nama, jenis_kelamin, lomba)

    return response
    
@app.post("/login")
async def login(
    username : str = Form(...),
    password : str = Form(...)
    ) :
    
    response = utils.login_verification(username, password)    

    return response

# Penanggung Jawab ==============================================================
# Auth Get Data 
@app.get("/register/pj")
async def getpj() :
    
    response = utils.get_pj_data()    

    return response

# Auth Delete Data 
@app.delete("/register/pj")
async def deletepj(uuid) :
    
    response = utils.delete_account_pj(uuid)    

    return response

# Auth Update Data 
@app.put("/register/pj")
async def updatepj(
    uuid : str = Form(...),
    username : str = Form(...),
    password : str = Form(...),
    nama : str = Form(...),
    jenis_kelamin : str = Form(...),
    lomba : str = Form(...)
    ) :
    
    response = utils.update_account_pj(uuid, username, password, nama, jenis_kelamin, lomba)    

    return response

# Get PJ Role 
@app.get("/pj/role")
async def rolepj(uuid):

    response = utils.get_role(uuid)

    return response

# Registration ===================================================================

## Single Category
@app.post("/single/")
async def add_single(
    id_user: Annotated[str, Form()],
    lomba: Annotated[str, Form()],
    asal_sekolah: Annotated[str, Form()],
    surat_tugas : Annotated[UploadFile, File()],
    no_telepon : Annotated[str, Form()],
    nama_lengkap : Annotated[str, Form()],
    jenis_kelamin : Annotated[str, Form()],
    alamat : Annotated[str, Form()],
    prestasi : Annotated[str, Form()],
    pas_photo : Annotated[UploadFile, File()],
    kartu_pelajar : Annotated[UploadFile, File()]
    ) :
    
    info = {        
        "id_user": id_user, 
        "nama" : nama_lengkap,
        "jenis_kelamin" : jenis_kelamin,
        "alamat" : alamat,
        "prestasi" : prestasi,
        "pas_photo" : pas_photo,
        "kartu_pelajar" : kartu_pelajar,
        "id_lomba" : lomba,
        "npsn" : asal_sekolah,
        "surat_tugas" : surat_tugas,
        "no_telp" : no_telepon
            }
    
    response = utils.single(info)

    return response

# Get Data
@app.get("/single/")
async def get_single(id_user) :
    
    response = utils.get_single_data(id_user)

    return response

@app.get("/single/all")
async def get_single_all() :
    
    response = utils.get_single_data_all()

    return response


## Team Category  
@app.post("/team/")
async def add_team(
    id_user: Annotated[str, Form()],
    lomba: Annotated[str, Form()],
    asal_sekolah: Annotated[str, Form()],
    surat_tugas : Annotated[UploadFile, File()],
    no_telepon : Annotated[str, Form()],
    nama_tim : Annotated[str, Form()],
    nama_pendamping : Annotated[str, Form()],

    nama_lengkap : Annotated[str, Form()],
    jenis_kelamin : Annotated[str, Form()],
    alamat : Annotated[str, Form()],
    prestasi : Annotated[str, Form()],
    pas_photo : Annotated[UploadFile, File()],
    kartu_pelajar : Annotated[UploadFile, File()],

    nama_lengkap_1 : Annotated[str, Form()],
    jenis_kelamin_1 : Annotated[str, Form()],
    alamat_1 : Annotated[str, Form()],
    prestasi_1 : Annotated[str, Form()],
    pas_photo_1 : Annotated[UploadFile, File()],
    kartu_pelajar_1 : Annotated[UploadFile, File()],

    nama_lengkap_2 : Annotated[str, Form()],
    jenis_kelamin_2 : Annotated[str, Form()],
    alamat_2 : Annotated[str, Form()],
    prestasi_2 : Annotated[str, Form()],
    pas_photo_2 : Annotated[UploadFile, File()],
    kartu_pelajar_2 : Annotated[UploadFile, File()],

    nama_lengkap_3 : Annotated[str, Form()],
    jenis_kelamin_3 : Annotated[str, Form()],
    alamat_3 : Annotated[str, Form()],
    prestasi_3 : Annotated[str, Form()],
    pas_photo_3 : Annotated[UploadFile, File()],
    kartu_pelajar_3 : Annotated[UploadFile, File()]
    ) :
    
    info = {        
        "uuid": id_user, 
        "id_lomba" : lomba,
        "npsn" : asal_sekolah,
        "surat_tugas" : surat_tugas,
        "no_telp" : no_telepon,
        "nama_tim" : nama_tim,
        "nama_pendamping" : nama_pendamping,

        "nama" : nama_lengkap,
        "jenis_kelamin" : jenis_kelamin,
        "alamat" : alamat,
        "prestasi" : prestasi,
        "pas_photo" : pas_photo,
        "kartu_pelajar" : kartu_pelajar,

        "nama_1" : nama_lengkap_1,
        "jenis_kelamin_1" : jenis_kelamin_1,
        "alamat_1" : alamat_1,
        "prestasi_1" : prestasi_1,
        "pas_photo_1" : pas_photo_1,
        "kartu_pelajar_1" : kartu_pelajar_1,

        "nama_2" : nama_lengkap_2,
        "jenis_kelamin_2" : jenis_kelamin_2,
        "alamat_2" : alamat_2,
        "prestasi_2" : prestasi_2,
        "pas_photo_2" : pas_photo_2,
        "kartu_pelajar_2" : kartu_pelajar_2,

        "nama_3" : nama_lengkap_3,
        "jenis_kelamin_3" : jenis_kelamin_3,
        "alamat_3" : alamat_3,
        "prestasi_3" : prestasi_3,
        "pas_photo_3" : pas_photo_3,
        "kartu_pelajar_3" : kartu_pelajar_3,
            }
    
    response = utils.team(info)

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
@app.get("/team/")
async def get_team(id_user) :
    
    response = utils.get_team_data(id_user)

    return response

@app.get("/team/all")
async def get_team() :
    
    response = utils.get_team_data_all()

    return response

# Get Number Register Basketball
# @app.get("/basketball/count")
# async def get_basketball_count() :
    
#     response = utils.get_basketball_count()

#     return response

# Get Number Register Photography
# @app.get("/photography/count")
# async def get_basketball_count() :
    
#     response = utils.get_photography_count()

#     return response

# Metadata
@app.get("/jenjang/")
async def get_jenjang() :
    
    response = utils.get_jenjang_data()

    return response

@app.get("/sekolah/")
async def get_sekolah(id) :
    
    response = utils.get_sekolah_data(id)

    return response

@app.get("/lomba/link")
async def get_lomba_link(id) :
    
    response = utils.get_lomba_link(id)

    return response

@app.post("/lomba/")
async def add_lomba(
    id_lomba : Annotated[str, Form()],
    nama_lomba : Annotated[str, Form()],
    biaya_registrasi : Annotated[int, Form()],
    date_start : Annotated[str, Form()],
    date_end : Annotated[str, Form()],
    description : Annotated[str, Form()],
    ilustrasi : Annotated[UploadFile, File()],
    kategori_lomba : Annotated[str, Form()]
    ) :
    
    response = utils.add_lomba_data(id_lomba, nama_lomba, biaya_registrasi, date_start, date_end, description, ilustrasi, kategori_lomba)

    return response

@app.get("/lomba/")
async def get_lomba(id) :
    
    response = utils.get_lomba_data(id)

    return response

@app.put("/lomba/")
async def update_lomba(
    id_lomba : str = Form(),
    nama_lomba : str = Form(),
    biaya_registrasi : str = Form(),
    date_start : str = Form(),
    date_end : str = Form(),
    description : str = Form(),
    ilustrasi : UploadFile = None,
    scoring_link : str = Form(),
    kategori_lomba : str = Form()
    ) :
    if ilustrasi.size == 0:
        ilustrasi = None

    response = utils.update_lomba_data(id_lomba, nama_lomba, biaya_registrasi, date_start, date_end, description, ilustrasi, kategori_lomba, scoring_link)

    return response

@app.delete("/lomba/")
async def delete_lomba(id_lomba) :
    
    response = utils.delete_lomba(id_lomba)

    return response

@app.get("/lomba/all")
async def get_lomba() :
    
    response = utils.get_lomba_all_data()

    return response

@app.get("/lomba/count")
async def get_count_lomba() :

    response = utils.get_count_lomba()

    return response

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=int(8000))