import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL missing")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_SERVICE_ROLE_KEY missing")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY[:20])

print("Supabase client initialized successfully")