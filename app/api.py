from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth.guest_auth import route_guest_auth
from routes.auth.member_auth import route_member_auth
from routes.work.guest_work import route_guest_work
from routes.work.member_work import route_member_work

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*", "*"],
    allow_methods=["*", "*"],
    allow_headers=["*", "*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(route_guest_auth)
app.include_router(route_member_auth)
app.include_router(route_member_work)
app.include_router(route_guest_work)
# app.include_router(route_admin_account)
# app.include_router(route_admin_book)
# app.include_router(route_admin_member)
# app.include_router(route_admin_borrowing)
# app.include_router(route_admin_fee)
