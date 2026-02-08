"""
JWT authentication middleware.

Verifies JWT tokens and extracts user_id for all protected endpoints.
"""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional

from ..config import settings


# HTTP Bearer token scheme
security = HTTPBearer()


def verify_jwt_middleware(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Verify JWT token and extract user_id.

    This function is used as a dependency for protected endpoints.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        user_id: Authenticated user ID from token

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token",
        )

    token = credentials.credentials

    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
        )

        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user_id",
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )


def get_current_user(user_id: str = Depends(verify_jwt_middleware)) -> str:
    """
    Dependency to get current authenticated user.

    Usage:
        @app.get("/endpoint")
        def endpoint(current_user: str = Depends(get_current_user)):
            # current_user contains the user_id from JWT
            pass

    Args:
        user_id: User ID from verified JWT token

    Returns:
        user_id: Authenticated user ID
    """
    return user_id


def verify_user_id_match(path_user_id: str, authenticated_user_id: str) -> None:
    """
    Verify that user_id in URL path matches authenticated user_id from JWT.

    CRITICAL SECURITY CHECK: Prevents cross-user data access.

    Args:
        path_user_id: User ID from URL path parameter
        authenticated_user_id: User ID from verified JWT token

    Raises:
        HTTPException: 403 if user IDs don't match
    """
    if path_user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: user_id mismatch",
        )
