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
def register_status(iduser):
    try :
        data, count = supabase.table('detail_akun').select('*').eq('uuid',iduser).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        if data[1] != [] :
            id_pendaftaran = data[1][0]['id_pendaftaran']
            query = text(f'''
                           SELECT 
                                    pendaftaran.id_pendaftaran as id_pendaftaran,
                                    pendaftaran.id_lomba as id_lomba,
                                    lomba.kategori_lomba as kategori_lomba
                            FROM 
                                    pendaftaran, lomba
                            WHERE
                                    pendaftaran.id_lomba = lomba.id_lomba
                                    AND
                                    pendaftaran.id_pendaftaran = '{id_pendaftaran}'
                            ''')

            # Execute the query with parameters
            with engine.connect() as conn:
                result = conn.execute(query)

            result = result.fetchall()
            # print(result[0][2])
            return {'status': "success", 'details': 'Registered', 'data': f'{result[0][2]}'}
        else :
            return {'status': "success", 'details': 'Not Registered', 'data': '-'}


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

def get_role(uuid):
    try :
        data, count = supabase.table('penanggung_jawab').select("id_lomba").eq('uuid', uuid).execute()
    
    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': '-', 'data' : data[1]}
        

def login_verification(username , password):
    try :
        data, count = supabase.table('akun').select('*').eq('username',username).execute()

    except Exception as Error:
        error = Error.json()['details']
        print(error)
        return {'status': "error", 'details': error}
    
    else :
        if data[1] == []:
            return {'status': "error", 'details': 'Akun Tidak Ditemukan'}
        
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
                lomba_data, count = supabase.table('lomba').select('kategori_lomba').eq('id_lomba ',pj_data[1][0]['id_lomba']).execute()

                if lomba_data[1][0]['kategori_lomba'] == 'team':
                    return {'status': "success", 'details': 'User verification success. Mengalihkan halaman....', 'data':[id_user, user], 'redirect': '../pj/team-pj.html'}
                else :
                    return {'status': "success", 'details': 'User verification success. Mengalihkan halaman....', 'data':[id_user, user], 'redirect': '../pj/single-pj.html'}
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


def single(information) :  
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
        
        data, count = supabase.table('single_member').insert(
            {"id_peserta": id + "-peserta", 
             "nama": information["nama"], 
             "jenis_kelamin": information["jenis_kelamin"], 
             "alamat": information["alamat"],
             "prestasi": information["prestasi"],
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

def team(information) :  
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
             "nama_pendamping": information["nama_pendamping"]
             }
             ).execute()   
             
        data, count = supabase.table('detail_registrasi_tim').insert(
            {"id_pendaftaran": id + "-pendaftaran", 
             "id_tim": id + "-tim"
             }
             ).execute()
                
        data, count = supabase.table('team_member').insert(
            {"id_peserta": id + "-peserta",
             "id_tim": id + "-tim",  
             "nama": information["nama"], 
             "jenis_kelamin": information["jenis_kelamin"], 
             "alamat": information["alamat"],
             "prestasi": information["prestasi"],
             "pas_photo": url_data["pas_photo"],
             "kartu_pelajar": url_data["kartu_pelajar"]
             }
             ).execute()
                
        data, count = supabase.table('team_member').insert(
            {"id_peserta": id + "-peserta_1",
             "id_tim": id + "-tim",
             "nama": information["nama_1"], 
             "jenis_kelamin": information["jenis_kelamin_1"], 
             "alamat": information["alamat_1"],
             "prestasi": information["prestasi_1"],
             "pas_photo": url_data["pas_photo_1"],
             "kartu_pelajar": url_data["kartu_pelajar_1"]
             }
             ).execute()
                
        data, count = supabase.table('team_member').insert(
            {"id_peserta": id + "-peserta_2",
             "id_tim": id + "-tim",  
             "nama": information["nama_2"], 
             "jenis_kelamin": information["jenis_kelamin_2"], 
             "alamat": information["alamat_2"],
             "prestasi": information["prestasi_2"],
             "pas_photo": url_data["pas_photo_2"],
             "kartu_pelajar": url_data["kartu_pelajar_2"]
             }
             ).execute()
                
        data, count = supabase.table('team_member').insert(
            {"id_peserta": id + "-peserta_3",
             "id_tim": id + "-tim",  
             "nama": information["nama_3"], 
             "jenis_kelamin": information["jenis_kelamin_3"], 
             "alamat": information["alamat_3"],
             "prestasi": information["prestasi_3"],
             "pas_photo": url_data["pas_photo_3"],
             "kartu_pelajar": url_data["kartu_pelajar_3"]
             }
             ).execute()
        
    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error-on-add", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil mendaftarkan peserta'}


# View
## Photography

def get_single_data(id_user):
    try :
        query = text(f'''
            SELECT 
            pendaftaran.id_pendaftaran as id_pendaftaran, 
            DATE(pendaftaran.date_created) as date,
            jenjang_sekolah.jenjang as jenjang,
            sekolah.nama_sekolah as nama_sekolah,
            pendaftaran.no_telp as no_telp,
            single_member.nama as nama_peserta,
            single_member.alamat as alamat_peserta,
            single_member.prestasi as prestasi_peserta,
            single_member.pas_photo as pas_photo,
            lomba.nama_lomba as nama_lomba,
            lomba.scoring_link as scoring_link
            FROM 
            pendaftaran, 
            lomba,
            sekolah,
            jenjang_sekolah,
            single_member,
            detail_registrasi_individu,
            detail_akun
            WHERE
            detail_akun.uuid = '{id_user}'
            AND 
            lomba.id_lomba = pendaftaran.id_lomba
            AND
            detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
            AND
            detail_registrasi_individu.id_pendaftaran = pendaftaran.id_pendaftaran
            AND
            detail_registrasi_individu.id_peserta = single_member.id_peserta
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
                    result[0][8],
                    result[0][9],
                    result[0][10],
                ]}
    
def get_single_data_all():
    try :
        query = text(f'''
            SELECT 
            pendaftaran.id_pendaftaran as id_pendaftaran, 
            DATE(pendaftaran.date_created) as date,
            jenjang_sekolah.jenjang as jenjang,
            sekolah.nama_sekolah as nama_sekolah,
            pendaftaran.no_telp as no_telp,
            single_member.nama as nama_peserta,
            single_member.alamat as alamat_peserta,
            single_member.prestasi as prestasi_peserta,
            single_member.pas_photo as pas_photo,
            pendaftaran.surat_tugas as surat_tugas,
            single_member.kartu_pelajar as kartu_pelajar,
            pendaftaran.id_lomba as id_lomba
            FROM 
            pendaftaran, 
            sekolah,
            jenjang_sekolah,
            single_member,
            detail_registrasi_individu,
            detail_akun
            WHERE
            detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
            AND
            detail_registrasi_individu.id_pendaftaran = pendaftaran.id_pendaftaran
            AND
            detail_registrasi_individu.id_peserta = single_member.id_peserta
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
            temp_dict['prestasi_peserta'] = participant[7]
            temp_dict['pas_photo'] = participant[8]
            temp_dict['surat_tugas'] = participant[9]
            temp_dict['kartu_pelajar'] = participant[10]
            temp_dict['id_lomba'] = participant[11]
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
# def get_basketball_count():
#     try:
#        data, count = supabase.table('pendaftaran').select('*', count='exact').eq('id_lomba', '150').execute()

#     except Exception as Error:
#         return {'status': "error", 'details': ['error-get',Error]}
    
#     else :
#         return {'status': "success", 
#                 'details': '-', 
#                 'data' : count[1]
#                 }


def get_team_data(id_user):
    try :
        query_general = text(f'''
            SELECT 
                pendaftaran.id_pendaftaran as id_pendaftaran, 
                DATE(pendaftaran.date_created) as date,
                jenjang_sekolah.jenjang as jenjang,
                sekolah.nama_sekolah as nama_sekolah,
                tim.nama_pendamping as pendamping,
                pendaftaran.no_telp as no_telp,
                lomba.nama_lomba as nama_lomba,
                lomba.scoring_link as scoring_link
            FROM 
                lomba,
                pendaftaran, 
                sekolah,
                jenjang_sekolah,
                tim,
                detail_registrasi_tim,
                detail_akun
            WHERE
                detail_akun.uuid = '{id_user}'
                AND
                lomba.id_lomba = pendaftaran.id_lomba
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
                team_member.nama as nama, 
                team_member.jenis_kelamin as jenis_kelamin,
                team_member.alamat as alamat,
                team_member.prestasi as prestasi,
                team_member.pas_photo as pas_photo,
                tim.nama_tim as nama_tim
            FROM 
                team_member, tim, detail_registrasi_tim, pendaftaran, detail_akun
            WHERE
                detail_akun.uuid = '{id_user}'
                AND
                detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
                AND
                detail_registrasi_tim.id_pendaftaran = pendaftaran.id_pendaftaran
                AND 
                detail_registrasi_tim.id_tim = tim.id_tim
                AND
                team_member.id_tim =  tim.id_tim
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
            temp_dict['jenis_kelamin'] = member[1]
            temp_dict['alamat'] = member[2]
            temp_dict['pas_photo'] = member[4]
            temp_dict['nama_lomba'] = member[5]
            temp_dict['prestasi'] = member[3]
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
                        'nama_pendamping' : result_general[0][4],
                        'no_telp' : result_general[0][5],
                        'nama_lomba' : result_general[0][6],
                        'scoring_link' : result_general[0][7]
                    },
                    'member' : wraper
                        }
                }
def get_team_data_all():
    try :
        query_general = text(f'''
            SELECT 
                pendaftaran.id_pendaftaran as id_pendaftaran, 
                DATE(pendaftaran.date_created) as date,
                jenjang_sekolah.jenjang as jenjang,
                sekolah.nama_sekolah as nama_sekolah,
                tim.nama_tim as nama_tim,
                tim.nama_pendamping as pendamping,
                pendaftaran.surat_tugas as surat_tugas,
                pendaftaran.no_telp as no_telp
            FROM 
                pendaftaran, 
                sekolah,
                jenjang_sekolah,
                tim,
                detail_registrasi_tim
            WHERE
                    pendaftaran.id_lomba = '150'
                AND
                    detail_registrasi_tim.id_pendaftaran = pendaftaran.id_pendaftaran
                AND
                    pendaftaran.npsn = sekolah.npsn
                AND 
                    sekolah.id_jenjang = jenjang_sekolah.id_jenjang
                AND 
                    tim.id_tim = detail_registrasi_tim.id_tim            
        ''')

        # Execute the query with parameters
        with engine.connect() as conn:
            result_general = conn.execute(query_general)

        result_general = result_general.fetchall()

        data = []
        for general in result_general:
            
            query_member = text(f'''
                    SELECT 
                        team_member.nama as nama, 
                        team_member.alamat as alamat,
                        team_member.prestasi as prestasi,
                        team_member.pas_photo as pas_photo,
                        team_member.kartu_pelajar as kartu_pelajar,
                        team_member.jenis_kelamin as jenis_kelamin
                    FROM 
                        team_member
                        
                    INNER JOIN
                        detail_registrasi_tim
                    ON  
                        detail_registrasi_tim.id_tim = team_member.id_tim
                    AND detail_registrasi_tim.id_pendaftaran = '{general[0]}'
                ''')

            with engine.connect() as conn:
                result_member = conn.execute(query_member)

            result_member = result_member.fetchall()
            
            member_wraper = []
            for member in result_member :
                # print(member[0])
                temp_dict = {
                    'nama_lengkap' : member[0],
                    'alamat' : member[1],
                    'prestasi' : member[2],
                    'pas_photo' : member[3],
                    'kartu_pelajar' : member[4],
                    'jenis_kelamin' : member[5]
                }
                # print(temp_dict)
                member_wraper.append(temp_dict)

            general = {
                'id_pendaftaran' : general[0],
                'date' : general[1],
                'jenjang' : general[2],
                'nama_sekolah' : general[3],
                'nama_tim' : general[4],
                'pendamping' : general[5],
                'surat_tugas' : general[6],
                'no_telp' : general[7],
                'member': member_wraper
                }

            data.append(general)

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : data
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
# Lomba
def add_lomba_data(id_lomba, nama_lomba, biaya_registrasi,  date_start, date_end, description, ilustrasi, kategori_lomba):
    try : 
        data = ilustrasi.file.read()
        file_name = f"{id_lomba}-{nama_lomba}.jpg" 
        supabase.storage.from_(f'registration-storage/ilustrasi_lomba').upload(file=data, path=file_name, file_options={"content-type" : "image/jpg"})
        public_url = supabase.storage.from_(f'registration-storage/ilustrasi_lomba').get_public_url(file_name)            

    except Exception as Error :
        return {'status': "error", 'details': 'error-upload'}

    try :
        data, count = supabase.table("lomba").insert({"id_lomba": id_lomba, "nama_lomba": nama_lomba,'biaya_registrasi':biaya_registrasi , "start_date":date_start, "end_date":date_end, 'description':description,'ilustrasi' : public_url, 'kategori_lomba':kategori_lomba}).execute()

    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}

    else :
        return {'status': "success", 
                'details': 'berhasil menambahkan lomba', 
                'data' : '-'
                }
    
def update_lomba_data(id_lomba, nama_lomba, biaya_registrasi, date_start, date_end, description, ilustrasi, kategori_lomba, scoring_link):
    try :
        temp_1 = {'nama_lomba':nama_lomba, 
                 'biaya_registrasi':biaya_registrasi, 
                 'start_date':date_start, 
                 'end_date':date_end, 
                 'description':description, 
                 'ilustrasi':ilustrasi, 
                 'kategori_lomba':kategori_lomba,
                 'scoring_link':scoring_link}
        temp = {}
        for key, item in temp_1.items():
           if temp_1[key] != None:
               temp[key] = item
        data, count =  supabase.table('lomba').update(temp).eq("id_lomba", id_lomba).execute()
    except Exception as Error:
        print(temp)
        print(Error)
        return {'status': "error", 'details': Error}

    else :
        return {'status': "success", 
                'details': '-', 
                'data' : data[1]
                }

def delete_lomba(id):
    try :
        data, count = supabase.table('lomba').delete().eq('id_lomba', id).execute()
        data, count = supabase.table('penanggung_jawab').delete().eq('id_lomba', id).execute()


    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': 'berhasil menghapus akun penanggung jawab'}

def get_lomba_data(id):
    try :
        query = text(f'''
            SELECT 
                lomba.nama_lomba as nama_lomba,
                lomba.biaya_registrasi as biaya, 
                lomba.kategori_lomba as kategori_lomba
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
                'data' : {'nama' : result[0][0], 'price':result[0][1], 'kategori_lomba':result[0][2]}
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
    

def get_count_lomba():
    try :
        query = text(f'''
                    SELECT 
                        count(pendaftaran.id_pendaftaran) as jumlah_pendaftar,
                        lomba.nama_lomba as nama_lomba,
                        lomba.kategori_lomba as kategori_lomba,
                        lomba.id_lomba as id
                    FROM 
                        pendaftaran, 
                        lomba
                    WHERE 
                        lomba.id_lomba = pendaftaran.id_lomba
                    GROUP BY 
                        nama_lomba,
                        kategori_lomba,
                        id
                ''')

        # Execute the query with parameters
        with engine.connect() as conn:
            result = conn.execute(query)
        result = result.fetchall()

        wraper = []
        for participant in result :
            temp_dict = {}
            temp_dict['jumlah_pendaftar'] = participant[0]
            temp_dict['nama_lomba'] = participant[1]
            temp_dict['kategori_lomba'] = participant[2]
            temp_dict['id_lomba'] = participant[3]
            wraper.append(temp_dict)
       

    except Exception as Error:
        return {'status': "error", 'details': ['error-get',Error]}
    
    else :
        return {'status': "success", 
                'details': '-', 
                'data' : 
                    wraper
                }

def get_lomba_link(idlomba):
    try :
        data, count = supabase.table('lomba').select("scoring_link").eq('id_lomba', idlomba).execute()
    
    except Exception as Error:
        error = Error.json()['details']
        return {'status': "error", 'details': error}
    
    else :
        return {'status': "success", 'details': '-', 'data' : data[1]}