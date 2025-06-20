from utils.faiss_utils import create_faiss_index_from_json
import os
from dotenv import load_dotenv

load_dotenv()

index = create_faiss_index_from_json("data/pitch_templates.json", os.getenv("GOOGLE_API_KEY"))
index.save_local("faiss_index")
print("FAISS index created successfully!")