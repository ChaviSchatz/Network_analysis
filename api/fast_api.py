import uvicorn
from fastapi import FastAPI

from api.auth_router import auth_router
from api.network_router import networks
from api.technician_router import technicians

app = FastAPI()
app.include_router(auth_router)
app.include_router(technicians)
app.include_router(networks)

uvicorn.run(app, host="127.0.0.1", port=3000)
