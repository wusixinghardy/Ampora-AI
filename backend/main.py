"""
Ampora AI Backend API
FastAPI server for video generation, authentication, and chat services
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import os
import uvicorn
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import stripe
from src.config import OPENAI_API_KEY, GEMINI_API_KEY
from pathlib import Path

# Optional Supabase import
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

# Initialize FastAPI app
app = FastAPI(title="Ampora AI API", version="1.0.0")

# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.github.io",  # For GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Optional[Client] = None

if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Warning: Supabase initialization failed: {e}")
        supabase = None

# Initialize Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe.api_key = STRIPE_SECRET_KEY

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Test mode - allows dev accounts to bypass payment and even skip DB/Stripe
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"
TEST_ACCOUNTS = ["testuser", "demo", "dev", "admin"]  # Accounts that bypass payment
TEST_MODE_NO_DB = os.getenv("TEST_MODE_NO_DB", "true").lower() == "true"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR.parent / "artifacts"


# ==================== Pydantic Models ====================

class UserLogin(BaseModel):
    username: str
    password: str

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    payment_intent_id: Optional[str] = None  # Stripe payment intent

class ChatMessage(BaseModel):
    message: str

class VideoRequest(BaseModel):
    topic: str


# ==================== Helper Functions ====================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(authorization: Optional[str] = Header(None)):
    """Dependency to get current user from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    return payload


# ==================== Authentication Endpoints ====================

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    """User login endpoint"""
    try:
        # In test mode without DB, allow hardcoded test accounts
        if TEST_MODE and TEST_MODE_NO_DB and user_data.username.lower() in TEST_ACCOUNTS:
            token = create_access_token({"sub": f"test-{user_data.username}", "username": user_data.username})
            return {
                "token": token,
                "user": {
                    "id": f"test-{user_data.username}",
                    "username": user_data.username,
                    "email": f"{user_data.username}@example.com"
                }
            }

        if supabase:
            # Query Supabase for user
            response = supabase.table("users").select("*").eq("username", user_data.username).execute()
            
            if not response.data:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            user = response.data[0]
            
            # Verify password
            if not verify_password(user_data.password, user["password_hash"]):
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            # Check subscription status
            if not user.get("is_active") and user["username"] not in TEST_ACCOUNTS:
                raise HTTPException(status_code=403, detail="Subscription expired. Please renew.")
            
            # Create token
            token = create_access_token({"sub": user["id"], "username": user["username"]})
            
            return {
                "token": token,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"]
                }
            }
        else:
            # Fallback if Supabase not configured
            raise HTTPException(status_code=503, detail="Database not configured. Set SUPABASE_URL/KEY or enable TEST_MODE_NO_DB=true.")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@app.post("/api/auth/signup")
async def signup(user_data: UserSignup):
    """User signup endpoint with Stripe payment"""
    try:
        # Verify Stripe payment if not test account
        if user_data.username not in TEST_ACCOUNTS and not TEST_MODE:
            if not STRIPE_SECRET_KEY:
                raise HTTPException(status_code=400, detail="Stripe not configured. Set STRIPE_SECRET_KEY or use TEST_MODE.")
            if not user_data.payment_intent_id:
                raise HTTPException(status_code=400, detail="Payment required")
            
            # Verify payment with Stripe
            try:
                payment_intent = stripe.PaymentIntent.retrieve(user_data.payment_intent_id)
                if payment_intent.status != "succeeded":
                    raise HTTPException(status_code=400, detail="Payment not completed")
            except stripe.error.StripeError as e:
                raise HTTPException(status_code=400, detail=f"Payment verification failed: {str(e)}")
        
        if supabase:
            # Check if user already exists
            existing = supabase.table("users").select("*").eq("username", user_data.username).execute()
            if existing.data:
                raise HTTPException(status_code=400, detail="Username already exists")
            
            existing_email = supabase.table("users").select("*").eq("email", user_data.email).execute()
            if existing_email.data:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # Hash password
            password_hash = get_password_hash(user_data.password)
            
            # Create user in Supabase
            new_user = {
                "username": user_data.username,
                "email": user_data.email,
                "password_hash": password_hash,
                "is_active": True,  # Active if payment verified or test account
                "subscription_expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat() if user_data.username not in TEST_ACCOUNTS else None,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = supabase.table("users").insert(new_user).execute()
            
            if result.data:
                user = result.data[0]
                token = create_access_token({"sub": user["id"], "username": user["username"]})
                
                return {
                    "token": token,
                    "user": {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"]
                    }
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to create user")
        else:
            # In test mode without DB, create fake user for test accounts only
            if TEST_MODE and TEST_MODE_NO_DB and user_data.username.lower() in TEST_ACCOUNTS:
                token = create_access_token({"sub": f"test-{user_data.username}", "username": user_data.username})
                return {
                    "token": token,
                    "user": {
                        "id": f"test-{user_data.username}",
                        "username": user_data.username,
                        "email": user_data.email
                    }
                }
            raise HTTPException(status_code=503, detail="Database not configured. Set SUPABASE_URL/KEY or enable TEST_MODE_NO_DB=true.")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


# ==================== Chat Endpoints ====================

@app.post("/api/chat")
async def chat(message: ChatMessage, current_user: dict = Depends(get_current_user)):
    """Chat endpoint - processes user messages and generates video"""
    try:
        # In pure test mode without AI keys, return a stubbed response so UI works
        if TEST_MODE and (not OPENAI_API_KEY or not GEMINI_API_KEY):
            return {
                "response": f"(Test mode) Generated a demo video for '{message.message}'.",
                "video_url": "/artifacts/Bubble_Sort_Algorithm.mp4",
                "topic": message.message
            }
        
        # Import video generation service
        from src.services.video import generate_lecture_video
        
        # Generate video (this is the expensive $4 operation)
        output_filename = f"generated_video_{current_user['sub']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_dir = "output/videos"
        output_path = os.path.join(output_dir, output_filename)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate video
        video_path = generate_lecture_video(message.message, output_path)
        
        # Return response with video URL
        video_url = f"/api/videos/{output_filename}"
        
        return {
            "response": f"I've generated a video lecture about '{message.message}'. The video is ready for download!",
            "video_url": video_url,
            "topic": message.message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")


# ==================== Video Endpoints ====================

@app.get("/api/videos/{filename}")
async def get_video(filename: str):
    """Serve generated video files"""
    video_path = os.path.join("output/videos", filename)
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=filename
    )


@app.get("/artifacts/{filename}")
async def get_artifact(filename: str):
    """Serve static artifacts like demo videos and logos"""
    artifact_path = ARTIFACTS_DIR / filename
    if not artifact_path.exists():
        raise HTTPException(status_code=404, detail="Artifact not found")
    # Infer media type
    media_type = "video/mp4" if filename.lower().endswith(".mp4") else "image/png"
    return FileResponse(artifact_path, media_type=media_type, filename=filename)


# ==================== Stripe Endpoints ====================

@app.post("/api/stripe/create-payment-intent")
async def create_payment_intent():
    """Create Stripe payment intent for subscription"""
    try:
        # If Stripe not configured and in test mode, return mock intent
        if TEST_MODE and (not STRIPE_SECRET_KEY):
            amount = float(os.getenv("STRIPE_SUBSCRIPTION_PRICE", "9.99"))
            return {
                "client_secret": "test_client_secret_mock",
                "payment_intent_id": "pi_test_mock",
                "amount": amount
            }

        if not STRIPE_SECRET_KEY:
            raise HTTPException(status_code=503, detail="Stripe not configured. Set STRIPE_SECRET_KEY or enable TEST_MODE.")

        # Get subscription price from environment (default $9.99/month)
        amount = int(float(os.getenv("STRIPE_SUBSCRIPTION_PRICE", "9.99")) * 100)  # Convert to cents
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            metadata={"subscription_type": "monthly"}
        )
        
        return {
            "client_secret": payment_intent.client_secret,
            "payment_intent_id": payment_intent.id,
            "amount": amount / 100  # Return in dollars
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment intent creation failed: {str(e)}")


# ==================== Health Check ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Ampora AI API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected" if supabase else ("test-mode-no-db" if TEST_MODE and TEST_MODE_NO_DB else "not configured"),
        "stripe": "configured" if STRIPE_SECRET_KEY else ("mock" if TEST_MODE else "not configured"),
        "test_mode": TEST_MODE,
        "test_mode_no_db": TEST_MODE_NO_DB
    }


# ==================== Run Server ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )

