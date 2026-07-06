from supabase_client import supabase

try:
    response = supabase.storage.list_buckets()
    print("Connected Successfully!")
    print(response)
    # test_storage.py


    print(supabase.storage.list_buckets())

except Exception as e:
    print("Connection Failed!")
    print(type(e))
    print(e)