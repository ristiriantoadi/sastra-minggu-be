from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

PWDCONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_member = OAuth2PasswordBearer(
    tokenUrl="member/auth/login", scheme_name="member_oauth2_schema"
)
