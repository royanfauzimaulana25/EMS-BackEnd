# # # # import uuid
# # # # import random
# # # # from fastapi import FastAPI, File, Form, UploadFile
# # # # from PIL import Image
# # # # import io
# # # # import uuid

# # # # id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'EMS-Youth'))

from supabase import create_client, Client
url : str = "http://mbqjqbrviyhkgsgkvevx.supabase.co"
key : str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1icWpxYnJ2aXloa2dzZ2t2ZXZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg0MjY0MzMsImV4cCI6MjAzNDAwMjQzM30._CAllqdbgfzcQ2N8aUmWVRRXPQZl7z_zkNLpu51wWEc"
supabase: Client = create_client(url, key)

username = 'vhsusanto@gmail.com'
data, count = supabase.table("akun").select("username").execute()
print(data)