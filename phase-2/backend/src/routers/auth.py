"""
Authentication router.

Handles user signup and login endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
import bcrypt
import jwt
from datetime import datetime, timedelta
import uuid

from ..database import get_session
from ..models import User
from ..schemas import SignupRequest, LoginRequest, AuthResponse
from ..config import settings


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """
    Register a new user account.

    Args:
        request: Signup request with email and password
        session: Database session

    Returns:
        AuthResponse with user_id, email, and JWT token

    Raises:
        HTTPException 400: Email already registered
    """
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    # Hash password
    password_bytes = request.password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    # Create user with UUID
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=request.email,
        password_hash=password_hash,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT token
    token = create_jwt_token(user.id)

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        token=token,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """
    Login with email and password.

    Args:
        request: Login request with email and password
        session: Database session

    Returns:
        AuthResponse with user_id, email, and JWT token

    Raises:
        HTTPException 401: Invalid email or password
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    # Verify password
    password_bytes = request.password.encode('utf-8')
    password_hash_bytes = user.password_hash.encode('utf-8')

    if not bcrypt.checkpw(password_bytes, password_hash_bytes):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    # Generate JWT token
    token = create_jwt_token(user.id)

    return AuthResponse(
        user_id=user.id,
        email=user.email,
        token=token,
    )


def create_jwt_token(user_id: str, exp_hours: int = 24) -> str:
    """
    Create JWT token for authenticated user.

    Args:
        user_id: User ID to include in token
        exp_hours: Token expiration in hours (default 24)

    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=exp_hours),
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(
        payload,
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256",
    )

    return token
