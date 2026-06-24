from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")

print("SUPABASE_URL =", SUPABASE_URL)
print("SUPABASE_KEY EXISTS =", SUPABASE_KEY is not None)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

BUCKET = os.getenv("BUCKET_NAME")

print("BUCKET =", BUCKET)