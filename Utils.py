# import sqlalchemy as sql
from supabase import create_client, Client
from datetime import datetime
import uuid
from sqlalchemy import create_engine, text
import time


# Connect Supabse via SQLAlchemy
URL = "postgresql://postgres.mbqjqbrviyhkgsgkvevx:#Ems.25qweerty#@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(URL, connect_args={"connect_timeout": "0"})

# Connect Supabase via API
url : str = "https://mbqjqbrviyhkgsgkvevx.supabase.co"
key : str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1icWpxYnJ2aXloa2dzZ2t2ZXZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg0MjY0MzMsImV4cCI6MjAzNDAwMjQzM30._CAllqdbgfzcQ2N8aUmWVRRXPQZl7z_zkNLpu51wWEc'
supabase: Client = create_client(url, key)

# Generate Random ID SHA
# id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'EMS-Youth' + str(time.time()))) 

def generate_uuid():
    return str(uuid.uuid4())

# Auth
def add_account(username, password, role):
    try :
        data, count = supabase.table('akun').insert({"username": username, "password": password, "role": role, "date_created": str(datetime.now())}).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil membuat akun'}
    

def login_verification(username , password):
    try :
        data, count = supabase.table('akun').select('*').eq('username',username).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        user = data[1][0]['username']
        pw = data[1][0]['password']
        id_user = data[1][0]['uuid']

        if username == user and password == pw :
            return {'status': "success", 'details': '-', 'data':id_user}
        else :
            return {'status': "error", 'details': 'Email / Password salah'}
        
# Registration

def photography(information) :  
    id = generate_uuid()

    # Upload File to storage
    url_data = {'surat_tugas' : '', 'pas_photo' : '' , 'kartu_pelajar' : ''}
    try : 
        for name in url_data.keys():
            data = information[name].file.read()
            if name == 'surat_tugas':
                file_name = f"{generate_uuid()}-{name}.pdf" 
                supabase.storage.from_(f'registration-storage/{name}').upload(file=data, path=file_name, file_options={"content-type" : "application/pdf"})
                public_url = supabase.storage.from_(f'registration-storage/{name}').get_public_url(file_name)
                url_data[name] = public_url
            else :
                file_name = f"{generate_uuid()}-{name}.jpg"
                supabase.storage.from_(f'registration-storage/{name}').upload(file=data, path=file_name, file_options={"content-type" : "image/jpg"})
                public_url = supabase.storage.from_(f'registration-storage/{name}').get_public_url(file_name)
                url_data[name] = public_url



    except Exception as Error :
        return {'status': "error", 'details': 'error-upload'}

    # Add data to database 
    try :
        data, count = supabase.table('pendaftaran').insert(
            {"id_pendaftaran": id + "-pendaftaran", 
             "id_lomba": information["id_lomba"], 
             "npsn": information["npsn"], 
             "surat_tugas": url_data["surat_tugas"],
             "no_telp": information["no_telp"],
             "date_created": str(datetime.now()),
             }
             ).execute()
        
        data, count = supabase.table('detail_akun').insert(
            {"uuid": information["id_user"], 
             "id_pendaftaran": id + "-pendaftaran"
             }
             ).execute()
        
        data, count = supabase.table('peserta_fotografi').insert(
            {"id_peserta": id + "-peserta", 
             "nama": information["nama"], 
             "jenis_kelamin": information["jenis_kelamin"], 
             "alamat": information["alamat"],
             "pas_photo": url_data["pas_photo"],
             "kartu_pelajar": url_data["kartu_pelajar"]
             }
             ).execute()
        
        data, count = supabase.table('detail_registrasi_individu').insert(
            {"id_pendaftaran": id + "-pendaftaran", 
             "id_peserta": id + "-peserta"
             }
             ).execute()        
        
    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil mendaftarkan peserta' , 'id' : id}

def basketball(information) :  
    id = generate_uuid()

    # Upload File to storage
    url_data = {'surat_tugas' : '', 
                'pas_photo' : '' , 
                'kartu_pelajar' : '',

                'pas_photo_1' : '' , 
                'kartu_pelajar_1' : '',

                'pas_photo_2' : '' , 
                'kartu_pelajar_2' : '',

                'pas_photo_3' : '' , 
                'kartu_pelajar_3' : ''
                }
    try : 
        for name in url_data.keys():
            data = information[name].file.read()
            if name == 'surat_tugas':
                file_name = f"{id}-{name}.pdf" 
                supabase.storage.from_(f'registration-storage/{name}').upload(file=data, path=file_name, file_options={"content-type" : "application/pdf"})
                public_url = supabase.storage.from_(f'registration-storage/{name}').get_public_url(file_name)
                url_data[name] = public_url
            elif name == 'pas_photo': 
                file_name = f"{id}-{name}.jpg"
                supabase.storage.from_(f'registration-storage/pas_photo').upload(file=data, path=file_name, file_options={"content-type" : "image/jpg"})
                public_url = supabase.storage.from_(f'registration-storage/{name}').get_public_url(file_name)
                url_data[name] = public_url
            elif name == 'kartu_pelajar':
                file_name = f"{id}-{name}.jpg"
                supabase.storage.from_(f'registration-storage/kartu_pelajar').upload(file=data, path=file_name, file_options={"content-type" : "image/jpg"})
                public_url = supabase.storage.from_(f'registration-storage/{name}').get_public_url(file_name)
                url_data[name] = public_url



    except Exception as Error :
        return {'status': "error", 'details': Error}

    # Add data to database 
    try :
        data, count = supabase.table('pendaftaran').insert(
            {"id_pendaftaran": id + "-pendaftaran", 
             "id_lomba": information["id_lomba"], 
             "npsn": information["npsn"], 
             "surat_tugas": url_data["surat_tugas"],
             "no_telp": information["no_telp"],
             "date_created": str(datetime.now()),
             }
             ).execute()
        
        data, count = supabase.table('detail_akun').insert(
            {"uuid": information["uuid"], 
             "id_pendaftaran": id + "-pendaftaran"
             }
             ).execute()
        
        
        data, count = supabase.table('tim').insert(
            {"id_tim": id + "-tim", 
             "nama_tim": information["nama_tim"], 
             "nama_pelatih": information["nama_tim"], 
             "nama_official": information["nama_official"], 
             }
             ).execute()   
             
        data, count = supabase.table('detail_registrasi_tim').insert(
            {"id_pendaftaran": id + "-pendaftaran", 
             "id_tim": id + "-tim"
             }
             ).execute()
                
        data, count = supabase.table('peserta_basket').insert(
            {"id_peserta": id + "-peserta",
             "id_tim": id + "-tim",  
             "nama": information["nama"], 
             "jenis_kelamin": information["jenis_kelamin"], 
             "alamat": information["alamat"],
             "no_punggung": information["no_punggung"],
             "pas_photo": url_data["pas_photo"],
             "kartu_pelajar": url_data["kartu_pelajar"],
             "is_captain": information["is_captain"]
             }
             ).execute()
                
        data, count = supabase.table('peserta_basket').insert(
            {"id_peserta": id + "-peserta_1",
             "nama": information["nama_1"], 
             "jenis_kelamin": information["jenis_kelamin_1"], 
             "alamat": information["alamat_1"],
             "no_punggung": information["no_punggung_1"],
             "pas_photo": url_data["pas_photo_1"],
             "kartu_pelajar": url_data["kartu_pelajar_1"],
             "id_tim": id + "-tim",  
             "is_captain": information["is_captain_1"]
             }
             ).execute()
                
        data, count = supabase.table('peserta_basket').insert(
            {"id_peserta": id + "-peserta_2",
             "id_tim": id + "-tim",  
             "nama": information["nama_2"], 
             "jenis_kelamin": information["jenis_kelamin_2"], 
             "alamat": information["alamat_2"],
             "no_punggung": information["no_punggung_2"],
             "pas_photo": url_data["pas_photo_2"],
             "kartu_pelajar": url_data["kartu_pelajar_2"],
             "is_captain": information["is_captain_2"]
             }
             ).execute()
                
        data, count = supabase.table('peserta_basket').insert(
            {"id_peserta": id + "-peserta_3",
             "id_tim": id + "-tim",  
             "nama": information["nama_3"], 
             "jenis_kelamin": information["jenis_kelamin_3"], 
             "alamat": information["alamat_3"],
             "no_punggung": information["no_punggung_3"],
             "pas_photo": url_data["pas_photo_3"],
             "kartu_pelajar": url_data["kartu_pelajar_3"],
             "is_captain": information["is_captain_3"]
             }
             ).execute()
        
    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error-on-add", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil mendaftarkan peserta'}


# View
## Photography

def get_photography_data(id_user):
    try :
        query = text(f'''
            SELECT 
            pendaftaran.id_pendaftaran as id_pendaftaran, 
            DATE(pendaftaran.date_created) as date,
            jenjang_sekolah.jenjang as jenjang,
            sekolah.nama_sekolah as nama_sekolah,
            pendaftaran.no_telp as no_telp,
            peserta_fotografi.nama as nama_peserta,
            peserta_fotografi.alamat as alamat_peserta,
            peserta_fotografi.pas_photo as pas_photo
            FROM 
            pendaftaran, 
            sekolah,
            jenjang_sekolah,
            peserta_fotografi,
            detail_registrasi_individu,
            detail_akun
            WHERE
            detail_akun.uuid = '{id_user}'
            AND
            detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
            AND
            detail_registrasi_individu.id_pendaftaran = pendaftaran.id_pendaftaran
            AND
            detail_registrasi_individu.id_peserta = peserta_fotografi.id_peserta
            AND
            pendaftaran.npsn = sekolah.npsn
            AND 
            sekolah.id_jenjang = jenjang_sekolah.id_jenjang
        ''')

        # Execute the query with parameters
        with engine.connect() as conn:
            result = conn.execute(query)

        result = result.fetchall()

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : [
                    result[0][0],
                    result[0][1],
                    result[0][2],
                    result[0][3],
                    result[0][4],
                    result[0][5],
                    result[0][6],
                    result[0][7],
                ]}
    
## Basketball

def get_basketball_data(id_user):
    try :
        query_general = text(f'''
            SELECT 
                pendaftaran.id_pendaftaran as id_pendaftaran, 
                DATE(pendaftaran.date_created) as date,
                jenjang_sekolah.jenjang as jenjang,
                sekolah.nama_sekolah as nama_sekolah,
                tim.nama_pelatih as pelatih,
                tim.nama_official as official,
                pendaftaran.no_telp as no_telp
            FROM 
                pendaftaran, 
                sekolah,
                jenjang_sekolah,
                tim,
                detail_registrasi_tim,
                detail_akun
            WHERE
                detail_akun.uuid = '{id_user}'
                AND
                detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
                AND
                detail_registrasi_tim.id_pendaftaran = pendaftaran.id_pendaftaran
                AND
                pendaftaran.npsn = sekolah.npsn
                AND 
                sekolah.id_jenjang = jenjang_sekolah.id_jenjang
        ''')

        query_member = text(f'''
           SELECT 
                peserta_basket.nama as nama, 
                peserta_basket.no_punggung as no_punggung,
                peserta_basket.alamat as alamat,
                peserta_basket.pas_photo as pas_photo,
                tim.nama_tim as nama_tim
            FROM 
                peserta_basket, tim, detail_registrasi_tim, pendaftaran, detail_akun
            WHERE
                detail_akun.uuid = '{id_user}'
                AND
                detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
                AND
                detail_registrasi_tim.id_pendaftaran = pendaftaran.id_pendaftaran
                AND 
                detail_registrasi_tim.id_tim = tim.id_tim
                AND
                peserta_basket.id_tim =  tim.id_tim
        ''')

        # Execute the query with parameters
        with engine.connect() as conn:
            result_general = conn.execute(query_general)
            result_member = conn.execute(query_member)

        result_general = result_general.fetchall()
        result_member = result_member.fetchall()

        wraper = []
        for member in result_member :
            temp_dict = {}
            temp_dict['nama_lengkap'] = member[0]
            temp_dict['no_punggung'] = member[1]
            temp_dict['alamat'] = member[2]
            temp_dict['pas_photo'] = member[3]
            wraper.append(temp_dict)

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : {
                    'general' : {
                        'id_pendaftaran' : result_general[0][0],
                        'date' : result_general[0][1],
                        'jenjang_sekolah' : result_general[0][2],
                        'nama_sekolah' : result_general[0][3],
                        'nama_pelatih' : result_general[0][4],
                        'nama_official' : result_general[0][5],
                        'no_telp' : result_general[0][6]
                    },
                    'member' : wraper
                        }
                }
