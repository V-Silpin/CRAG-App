from fastapi import FastAPI
from api.routes import router

app = FastAPI()

# Include the router with a prefix if needed
app.include_router(router, prefix="")

# You can also add other routes or middleware here if needed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)