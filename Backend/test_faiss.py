import sys
try:
    print("Importing FAISS...")
    from langchain_community.vectorstores import FAISS
    print("FAISS imported successfully.")
    with open("faiss_status.txt", "w") as f:
        f.write("SUCCESS")
except Exception as e:
    print(f"Error importing FAISS: {e}")
    with open("faiss_status.txt", "w") as f:
        f.write(f"ERROR: {e}")
