from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import models, schemas
from ..dependencies import get_db_session
from .security import get_password_hash, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    # ... (code from previous step)
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- NEW: Login Endpoint ---
@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    """Authenticates user and returns a JWT access token."""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .. import models, dependencies # Import models and dependencies

# ... (existing code from previous step) ...

# --- NEW: JWT Verification and User Retrieval ---
# This tells FastAPI where to look for the token ("tokenUrl" is our login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(dependencies.get_db_session)):
    """Decodes JWT, validates credentials, and returns the user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db_session
from ..auth.security import get_current_user

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
    dependencies=[Depends(get_current_user)] # Protect all routes in this file
)

@router.post("/", response_model=schemas.Address, status_code=status.HTTP_201_CREATED)
def create_address(
    address: schemas.AddressCreate, 
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user)
):
    """
    Adds a new address to be monitored for the authenticated user.
    """
    new_address = models.Address(**address.dict(), owner_id=current_user.id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address
