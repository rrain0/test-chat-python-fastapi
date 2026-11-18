from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Создаем схему безопасности
bearer_auth_scheme = HTTPBearer()

BearerAuthSchemeDep = Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth_scheme)]
