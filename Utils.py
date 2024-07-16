# import sqlalchemy as sql
from supabase import create_client, Client
from datetime import datetime
import uuid
from sqlalchemy import create_engine, text
import time
import os

# Connect Supabse via SQLAlchemy
URL = os.environ.get('sql_alchemy_supabase_url')

engine = create_engine(URL, connect_args={"connect_timeout": "0"})

# Connect Supabase via API
url : str = os.environ.get('supabase_api_url')
key : str = os.environ.get('supabase_api_key')


supabase: Client = create_client(url, key)

def generate_uuid():
    return str(uuid.uuid4())

# Auth
def add_account(username, password, role):
    try :
        data, count = supabase.table('akun').insert({"username": username, "password": password, "role": role, "date_created": str(datetime.now()), "uuid": generate_uuid()}).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil membuat akun'}

def add_account_pj(username, password, nama, jenis_kelamin, lomba):
    try :
        uuid = generate_uuid()
        data, count = supabase.table('akun').insert({"username": username, "password": password, "role": 'Penanggung Jawab', "date_created": str(datetime.now()), "uuid": uuid}).execute()
        data, count = supabase.table('penanggung_jawab').insert({"uuid": uuid, "nama": nama, "jenis_kelamin": jenis_kelamin, "id_lomba": lomba}).execute()


    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil membuat akun penanggung jawab'}

def delete_account_pj(uuid):
    try :
        data, count = supabase.table('penanggung_jawab').delete().eq('uuid', uuid).execute()
        data, count = supabase.table('akun').delete().eq('uuid', uuid).execute()


    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil menghapus akun penanggung jawab'}
    
def update_account_pj(uuid, username, password, nama, jenis_kelamin, lomba):
    try :
        data, count = supabase.table('penanggung_jawab').update({"nama": nama, "jenis_kelamin": jenis_kelamin, "id_lomba": lomba}).eq('uuid', uuid).execute()
        data, count = supabase.table('akun').update({"username": username, "password": password}).eq('uuid', uuid).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil mengupdate akun penanggung jawab'}
    

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
        role = data[1][0]['role']

        if username == user and password == pw :
            if role == 'Peserta':
                return {'status': "success", 'details': 'User verification success. Mengalihkan halaman....', 'data':[id_user, user], 'redirect': '../registration/competition-option.html'}
            elif role == 'Administrator' :
                return {'status': "success", 'details': 'User verification success. Mengalihkan halaman....', 'data':[id_user, user], 'redirect': '../admin/index.html'}
            elif role == 'Penanggung Jawab' :
                pj_data, count = supabase.table('penanggung_jawab').select('*').eq('uuid',id_user).execute()

                print(pj_data[1][0]['id_lomba'])
                if pj_data[1][0]['id_lomba'] == '150':
                    return {'status': "success", 'details': 'User verification success. Mengalihkan halaman....', 'data':[id_user, user], 'redirect': '../pj/basketball-pj.html'}
                else :
                    return {'status': "success", 'details': 'User verification success. Mengalihkan halaman....', 'data':[id_user, user], 'redirect': '../pj/photography-pj.html'}
            else :
                pass
        else :
            return {'status': "error", 'details': 'Email / Password salah'}

def get_pj_data ():
    try :
        query = text(f'''
           SELECT 
                penanggung_jawab.uuid as uuid,
                akun.username as username,
                akun.password as password_akun,
                penanggung_jawab.nama as nama,
                penanggung_jawab.jenis_kelamin as jenis_kelamin,
                lomba.nama_lomba as nama_lomba
            FROM 
                lomba, penanggung_jawab, akun
            WHERE 
                penanggung_jawab.id_lomba = lomba.id_lomba 
            AND
                akun.uuid = penanggung_jawab.uuid
        ''')

        # Execute the query with parameters
        with engine.connect() as conn:
            result = conn.execute(query)

        result = result.fetchall()

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        wraper = []
        for item in result :
            temp_dict = {}
            temp_dict['uuid'] = item[0]
            temp_dict['username'] = item[1]
            temp_dict['password'] = item[2]
            temp_dict['nama'] = item[3]
            temp_dict['jenis_Kelamin'] = item[4]
            temp_dict['nama_lomba'] = item[5]
            wraper.append(temp_dict)

        pass
        return {'status': "success", 
                'details': '-', 
                'data' : wraper
                }
        
# Registration
## Basketball Count
def get_photography_count():
    try:
       data, count = supabase.table('pendaftaran').select('*', count='exact').eq('id_lomba', '110').execute()

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : count[1]
                }


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
            if name[0:11] == 'surat_tugas':
                file_name = f"{id}-{name}.pdf" 
                supabase.storage.from_(f'registration-storage/{name}').upload(file=data, path=file_name, file_options={"content-type" : "application/pdf"})
                public_url = supabase.storage.from_(f'registration-storage/surat_tugas').get_public_url(file_name)
                url_data[name] = public_url
            elif name[0:9] == 'pas_photo': 
                file_name = f"{id}-{name}.jpg"
                supabase.storage.from_(f'registration-storage/pas_photo').upload(file=data, path=file_name, file_options={"content-type" : "image/jpg"})
                public_url = supabase.storage.from_(f'registration-storage/pas_photo').get_public_url(file_name)
                url_data[name] = public_url
            elif name[0:13] == 'kartu_pelajar':
                file_name = f"{id}-{name}.jpg"
                supabase.storage.from_(f'registration-storage/kartu_pelajar').upload(file=data, path=file_name, file_options={"content-type" : "image/jpg"})
                public_url = supabase.storage.from_(f'registration-storage/kartu_pelajar').get_public_url(file_name)
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
             "kategori_tim": information["kategori_tim"], 
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
    
def get_photography_data_all():
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
            peserta_fotografi.pas_photo as pas_photo,
            pendaftaran.surat_tugas as surat_tugas,
            peserta_fotografi.kartu_pelajar as kartu_pelajar
            FROM 
            pendaftaran, 
            sekolah,
            jenjang_sekolah,
            peserta_fotografi,
            detail_registrasi_individu,
            detail_akun
            WHERE
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

        wraper = []
        for participant in result :
            temp_dict = {}
            temp_dict['id_pendaftaran'] = participant[0]
            temp_dict['date'] = participant[1]
            temp_dict['jenjang_sekolah'] = participant[2]
            temp_dict['nama_sekolah'] = participant[3]
            temp_dict['no_telp'] = participant[4]
            temp_dict['nama_peserta'] = participant[5]
            temp_dict['alamat_peserta'] = participant[6]
            temp_dict['pas_photo'] = participant[7]
            temp_dict['surat_tugas'] = participant[8]
            temp_dict['kartu_pelajar'] = participant[9]
            wraper.append(temp_dict)
       

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : 
                    wraper
                }
    
## Basketball Count
def get_basketball_count():
    try:
       data, count = supabase.table('pendaftaran').select('*', count='exact').eq('id_lomba', '150').execute()

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : count[1]
                }


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
                tim.kategori_tim as kategori_tim,
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
                        'kategori_tim' : result_general[0][6],
                        'no_telp' : result_general[0][7]
                    },
                    'member' : wraper
                        }
                }
def get_basketball_data_all():
    try :
        query_general = text(f'''
            SELECT 
                pendaftaran.id_pendaftaran as id_pendaftaran, 
                DATE(pendaftaran.date_created) as date,
                jenjang_sekolah.jenjang as jenjang,
                sekolah.nama_sekolah as nama_sekolah,
                tim.nama_pelatih as pelatih,
                tim.nama_official as official,
                tim.kategori_tim as kategori_tim,
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
                        'kategori_tim' : result_general[0][6],
                        'no_telp' : result_general[0][7]
                    },
                    'member' : wraper
                        }
                }

# Payments 


def payBill(information):
    try :
        data, count = supabase.table('detail_akun').select('id_pendaftaran').eq('uuid', information['uuid']).execute()

        data, count = supabase.table('pembayaran').insert(
            {"id_bayar": information["id_bayar"], 
             "id_pendaftaran": data[1][0]["id_pendaftaran"],   
             "metode_pembayaran": information["metode_pembayaran"], 
             "jumlah_bayar": information["jumlah_bayar"], 
             "date_created": str(datetime.now())
             }
             ).execute()
    except Exception as Error:
        print(Error)
        return {'status': "error-on-add", 'details': Error}
    
    else :
        return {'status': "success", 'details': 'berhasil mencatat pembayaran'}

# Metadata
def get_jenjang_data():
    try :
        data, count = supabase.table('jenjang_sekolah').select('*').execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}

    else :
        data = data[1]
        return {'status': "success", 
                'details': '-', 
                'data' : data
                }
    
def get_sekolah_data(id):
    try :
        data, count = supabase.table('sekolah').select('*').eq('id_jenjang', id).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}

    else :
        data = data[1]
        return {'status': "success", 
                'details': '-', 
                'data' : data
                }
    
def get_lomba_data(id):
    try :
        query = text(f'''
            SELECT 
                lomba.nama_lomba as nama_lomba,
                lomba.biaya_registrasi as biaya
            FROM
                detail_akun, pendaftaran, lomba
            WHERE
                detail_akun.uuid = '{id}'
                AND
                detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran
                AND
                pendaftaran.id_lomba = lomba.id_lomba
        ''')

        # Execute the query with parameters
        with engine.connect() as conn:
            result = conn.execute(query)
        result = result.fetchall()

    except Exception as Error:
        return {'status': "error", 'details': Error}

    else :
        return {'status': "success", 
                'details': '-', 
                'data' : {'nama' : result[0][0], 'price':result[0][1]}
                }


def get_lomba_all_data():
    try :
       data, count = supabase.table('lomba').select('*').execute()
       
    except Exception as Error:
        return {'status': "error", 'details': Error}

    else :
        return {'status': "success", 
                'details': '-', 
                'data' : data[1]
                }
    
def update_lomba_data(id_lomba, start_date, end_date):
    try :
       data, count =  supabase.table('lomba').update({'start_date':start_date, 'end_date':end_date}).eq("id_lomba", id_lomba).execute()
       
    except Exception as Error:
        return {'status': "error", 'details': Error}

    else :
        return {'status': "success", 
                'details': '-', 
                'data' : data[1]
                }