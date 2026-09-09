from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference

from app.auth.router import router as auth_router
from app.profile.router import router as profile_router

app = FastAPI(title="Fitness App API")

app.include_router(auth_router)
app.include_router(profile_router)

add_scalar_reference(
    app,
    route="/scalar",
)


@app.get("/")
def hello_world():
    return {"message": "Hello from Excerises!"}
