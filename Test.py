# # # # import uuid
# # # # import random
from supabase import create_client, Client
# # # # from fastapi import FastAPI, File, Form, UploadFile
# # # # from PIL import Image
# # # # import io
# # # # import uuid

# # # # id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'EMS-Youth'))

# # # # url : str = "https://mbqjqbrviyhkgsgkvevx.supabase.co"
# # # # key : str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1icWpxYnJ2aXloa2dzZ2t2ZXZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg0MjY0MzMsImV4cCI6MjAzNDAwMjQzM30._CAllqdbgfzcQ2N8aUmWVRRXPQZl7z_zkNLpu51wWEc'
# # # # supabase: Client = create_client(url, key)

# # # # def photography(information) :   
        
# # # #     # with open(information["surat_tugas"].file) as f :
# # # #     #             supabase.storage.from_('registration-storage').upload(file=f, path="surat-tugas", file_options={"content-type" : "application/pdf"})

# # # #     image_data = information["surat_tugas"].file.read()
# # # #     file_name = f"{id}-surat.pdf"
# # # #     supabase.storage.from_('registration-storage/surat_tugas').upload(file=image_data, path=file_name, file_options={"content-type" : "application/pdf"})
# # # #     public_url = supabase.storage.from_('registration-storage/surat_tugas').get_public_url(file_name)
# # # #     print(public_url)

# # # # url_data = {'surat_tugas' : '', 'pas_photo' : '' , 'kartu_pelajar' : ''}

# # # # for item in url_data.keys() :
# # # #     url_data[item] = 'add'

# # # # print(url_data)
# # from sqlalchemy import create_engine, text

# # URL = "postgresql://postgres.mbqjqbrviyhkgsgkvevx:#Ems.25qweerty#@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
# # engine = create_engine(URL, connect_args={"connect_timeout": "0"})

# # id_user = '123456'
# # query_general = text(f'''
# #             SELECT 
# #                 pendaftaran.id_pendaftaran as id_pendaftaran, 
# #                 DATE(pendaftaran.date_created) as date,
# #                 jenjang_sekolah.jenjang as jenjang,
# #                 sekolah.nama_sekolah as nama_sekolah,
# #                 tim.nama_pelatih as pelatih,
# #                 tim.nama_official as official,
# #                 pendaftaran.no_telp as no_telp
# #             FROM 
# #                 pendaftaran, 
# #                 sekolah,
# #                 jenjang_sekolah,
# #                 tim,
# #                 detail_registrasi_tim,
# #                 detail_akun
# #             WHERE
# #                 detail_akun.uuid = '{id_user}'
# #                 AND
# #                 detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
# #                 AND
# #                 detail_registrasi_tim.id_pendaftaran = pendaftaran.id_pendaftaran
# #                 AND
# #                 pendaftaran.npsn = sekolah.npsn
# #                 AND 
# #                 sekolah.id_jenjang = jenjang_sekolah.id_jenjang
# #         ''')

# # query_member = text(f'''
# #             SELECT 
# #                 peserta_basket.nama as nama, 
# #                 peserta_basket.no_punggung as no_punggung,
# #                 peserta_basket.alamat as alamat,
# #                 peserta_basket.pas_photo as pas_photo,
# #                 tim.nama_tim as nama_tim
# #             FROM 
# #                 peserta_basket, tim, detail_registrasi_tim, pendaftaran, detail_akun
# #             WHERE
# #                 detail_akun.uuid = '{id_user}'
# #                 AND
# #                 detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran 
# #                 AND
# #                 detail_registrasi_tim.id_pendaftaran = pendaftaran.id_pendaftaran
# #                 AND 
# #                 detail_registrasi_tim.id_tim = tim.id_tim
# #                 AND
# #                 peserta_basket.id_tim =  tim.id_tim
# #         ''')

# # # Execute the query with parameters
# # with engine.connect() as conn:
# #     result_general = conn.execute(query_general)
# #     result_member = conn.execute(query_member)

# # result_general = result_general.fetchall()
# # result_member = result_member.fetchall()

# # print(result_general)
# # print(result_member)

# # # print({'status': "error", 'details': ['error-get']})
# # # print({'status': "error", 'details':result})

# # wraper = []
# # members = [('edward', '2', 'a', 'https://mbqjqbrviyhkgsgkvevx.supabase.co/storage/v1/object/public/registration-storage/pas_photo/0d8ce4f5-c569-5a78-839b-be010509909b-pas_photo.jpg', 'Tim YP'), 
# #         ('asd', '12', 'a', 'https://mbqjqbrviyhkgsgkvevx.supabase.co/storage/v1/object/public/registration-storage/pas_photo_1/0d8ce4f5-c569-5a78-839b-be010509909b-pas_photo_1.jpg', 'Tim YP'), 
# #         ('sad', '31', 'AS', 'https://mbqjqbrviyhkgsgkvevx.supabase.co/storage/v1/object/public/registration-storage/pas_photo_2/0d8ce4f5-c569-5a78-839b-be010509909b-pas_photo_2.jpg', 'Tim YP'), 
# #         ('asd', '45', 'asda', 'https://mbqjqbrviyhkgsgkvevx.supabase.co/storage/v1/object/public/registration-storage/pas_photo_3/0d8ce4f5-c569-5a78-839b-be010509909b-pas_photo_3.jpg', 'Tim YP')]
# # for member in members :
# #     temp_dict = {}
# #     temp_dict['nama_lengkap'] = member[0]
# #     temp_dict['no_punggung'] = member[1]
# #     temp_dict['alamat'] = member[2]
# #     temp_dict['pas_photo'] = member[3]
# #     wraper.append(temp_dict)

# # print(wraper)

# # import uuid
# # from datetime import datetime

# # id = str(uuid.uuid5(uuid.NAMESPACE_URL, 'EMS-Youth' + str(datetime.now()))) 
# # print(uuid.uuid4())
from sqlalchemy import create_engine, text

# # # Connect Supabase via API
url : str = "https://mbqjqbrviyhkgsgkvevx.supabase.co"
key : str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1icWpxYnJ2aXloa2dzZ2t2ZXZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg0MjY0MzMsImV4cCI6MjAzNDAwMjQzM30._CAllqdbgfzcQ2N8aUmWVRRXPQZl7z_zkNLpu51wWEc'
supabase: Client = create_client(url, key)

URL = "postgresql://postgres.mbqjqbrviyhkgsgkvevx:#Ems.25qweerty#@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(URL, connect_args={"connect_timeout": "0"})

# query_general = text(f'''
#             SELECT 
#                 lomba.nama_lomba as nama_lomba,
#                 lomba.biaya_registrasi as biaya
#             FROM
#                 detail_akun, pendaftaran, lomba
#             WHERE
#                 detail_akun.uuid = 'b5010442-8d98-41da-97dd-a7a9976d5f0e' 
#                 AND
#                 detail_akun.id_pendaftaran = pendaftaran.id_pendaftaran
#                 AND
#                 pendaftaran.id_lomba = lomba.id_lomba
#         ''')
#         # Execute the query with parameters
# with engine.connect() as conn:
#     result = conn.execute(query_general)

# result = result.fetchall()

# print(result)

# a = 'surat_tugas'
# b = 'pas_photo_1'
# c = 'kartu_pelajar'

# print(len(a))
# print(len(b))
# print(len(c))

# print('surat_tugas' == a[0:11])
# print('pas_photo' == b[0:9])
# print('kartu_pelajar' == c[0:13])

# data, count = supabase.table('lomba').select('*').execute()
# # print(count[1])
# wraper = []
# for item in data[1]:
#     wraper.append(item)
# print(type(data[1]))


query_general = text(f'''
    SELECT 
        pendaftaran.id_pendaftaran as id_pendaftaran, 
        DATE(pendaftaran.date_created) as date,
        jenjang_sekolah.jenjang as jenjang,
        sekolah.nama_sekolah as nama_sekolah,
        tim.nama_tim as nama_tim,
        tim.nama_pelatih as pelatih,
        tim.nama_official as official,
        tim.kategori_tim as kategori_tim,
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
                peserta_basket.nama as nama, 
                peserta_basket.no_punggung as no_punggung,
                peserta_basket.alamat as alamat,
                peserta_basket.pas_photo as pas_photo,
                peserta_basket.kartu_pelajar as kartu_pelajar
            FROM 
                peserta_basket
                
            INNER JOIN
                detail_registrasi_tim
            ON  
                detail_registrasi_tim.id_tim = peserta_basket.id_tim
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
            'no_punggung' : member[1],
            'alamat' : member[2],
            'pas_photo' : member[3],
            'kartu_pelajar' : member[4]
        }
        # print(temp_dict)
        member_wraper.append(temp_dict)

    general = {
        'id_pendaftaran' : general[0],
        'date' : general[1],
        'jenjang' : general[2],
        'nama_sekolah' : general[3],
        'nama_tim' : general[4],
        'pelatih' : general[5],
        'official' : general[6],
        'kategori_tim' : general[7],
        'no_telp' : general[8],
        'member': member_wraper
        }

    data.append(general)

print(data)
