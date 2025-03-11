from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins if set to ["*"]
    allow_credentials=True,
    allow_methods=["POST"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the router with a prefix if needed
app.include_router(router, prefix="")

# You can also add other routes or middleware here if needed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)