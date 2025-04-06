import os
import dotenv

dotenv.load_dotenv()

# a "URL DO FRONT" é o localhost fornecido pelo front-end. ( Ex: http://localhost:5173 )
config = {
    "client_url": "http://localhost:5173/" if os.getenv("ENVIRONMENT") == "dev" else ""
}