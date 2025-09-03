from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import models
from .database import engine
from .api.v1.routes import post, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    
)

app.include_router(authentication.router)
app.include_router(post.public_router)
app.include_router(post.protected_router)
app.include_router(user.public_router)
app.include_router(user.protected_router)



class Test():
    @app.get('/test')
    def test():
        return 2*[2] + [2]