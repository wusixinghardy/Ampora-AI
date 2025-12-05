# Technology Stack & Architecture Explanation

This document explains all technologies and how the system works, perfect for investor presentations and technical documentation.

---

## 🏗️ Architecture Overview

**Three-Tier Architecture:**
1. **Frontend (React)** - User interface
2. **Backend (FastAPI)** - API server and business logic
3. **Database (Supabase)** - User data and authentication
4. **Payment (Stripe)** - Subscription management

---

## 💻 Frontend Technologies

### React 18
- **What it is:** JavaScript library for building user interfaces
- **Why we use it:** Industry standard, component-based, fast rendering
- **How it works:** Breaks UI into reusable components (Login, Chat, Video Player)

### Vite
- **What it is:** Modern build tool and dev server
- **Why we use it:** Lightning-fast hot module replacement, optimized builds
- **How it works:** Serves files during development, bundles for production

### React Router DOM
- **What it is:** Navigation library for React
- **Why we use it:** Enables multi-page navigation without page reloads
- **How it works:** Manages routes (/, /login, /dashboard) and redirects

### React Icons
- **What it is:** Icon library
- **Why we use it:** Beautiful, consistent icons (user, lock, download, etc.)

---

## 🔧 Backend Technologies

### FastAPI (Python)
- **What it is:** Modern Python web framework for building APIs
- **Why we use it:** Fast, automatic API documentation, type validation
- **How it works:** 
  - Receives HTTP requests from frontend
  - Processes business logic
  - Returns JSON responses
  - Example: `/api/chat` endpoint receives message, generates video, returns video URL

### Python
- **What it is:** Programming language
- **Why we use it:** Excellent for AI/ML, large ecosystem, easy integration with AI services

### Uvicorn
- **What it is:** ASGI server (runs FastAPI)
- **Why we use it:** High performance, handles concurrent requests
- **How it works:** Listens on port 5000, serves API requests

---

## 🤖 AI Services

### OpenAI GPT-4
- **What it is:** Large language model for text generation
- **Why we use it:** Generates lecture content, scripts, explanations
- **How it works:** 
  - User sends: "Explain machine learning"
  - GPT-4 generates: Learning objectives, slide content, scripts
  - Cost: ~$0.10-0.50 per video (varies by length)

### Google Gemini
- **What it is:** AI model for image generation
- **Why we use it:** Creates slide visuals and diagrams
- **How it works:**
  - Receives description: "Diagram showing neural network layers"
  - Generates: High-quality image
  - Cost: ~$0.05-0.20 per image

### MoviePy
- **What it is:** Python library for video editing
- **Why we use it:** Combines images, audio, text into final video
- **How it works:**
  - Takes generated images
  - Adds voiceover audio
  - Syncs timing
  - Exports MP4 file
  - **Total Cost: ~$4 per video** (OpenAI + Gemini + processing)

---

## 🗄️ Database & Authentication

### Supabase
- **What it is:** Open-source Firebase alternative (PostgreSQL database)
- **Why we use it:** 
  - Secure user authentication
  - Scalable database
  - Real-time capabilities
  - Free tier available
- **How it works:**
  - Stores user accounts (username, email, hashed passwords)
  - Tracks subscription status
  - Provides secure API access
  - **Login Flow:**
    1. User enters username/password
    2. Frontend sends to backend
    3. Backend queries Supabase
    4. Verifies password hash
    5. Returns JWT token
    6. Frontend stores token for future requests

### JWT (JSON Web Tokens)
- **What it is:** Secure token-based authentication
- **Why we use it:** Stateless, secure, works across servers
- **How it works:**
  - User logs in → Backend creates token
  - Token contains: user ID, username, expiration
  - Frontend sends token with every API request
  - Backend verifies token before processing

### Password Hashing (bcrypt)
- **What it is:** One-way encryption for passwords
- **Why we use it:** Security - passwords never stored in plain text
- **How it works:**
  - User creates password: "mypassword123"
  - Backend hashes: "$2b$12$xyz..." (one-way, can't reverse)
  - Stored in database
  - Login: Hash input password, compare with stored hash

---

## 💳 Payment Processing

### Stripe
- **What it is:** Payment processing platform
- **Why we use it:** 
  - Industry standard
  - Easy integration
  - Handles subscriptions automatically
  - PCI compliant (we never touch card data)
- **How it works:**
  1. User clicks "Sign Up"
  2. Frontend creates payment intent via backend
  3. Stripe returns secure payment form
  4. User enters card details (sent directly to Stripe)
  5. Stripe processes payment
  6. Backend verifies payment succeeded
  7. Account created with active subscription
  8. **Monthly billing:** Stripe automatically charges each month

### Subscription Model
- **Price:** Configurable (default $9.99/month)
- **Change price:** Edit `STRIPE_SUBSCRIPTION_PRICE` in backend `.env`
- **Billing:** Automatic monthly recurring
- **Cancellation:** User can cancel anytime (handled by Stripe)

---

## 🔐 Security Features

### Authentication Flow:
```
1. User → Login Form
2. Frontend → POST /api/auth/login (username, password)
3. Backend → Query Supabase for user
4. Backend → Verify password hash
5. Backend → Create JWT token
6. Backend → Return token to frontend
7. Frontend → Store token in localStorage
8. Future requests → Include token in Authorization header
```

### Authorization Flow:
```
1. User → Sends chat message
2. Frontend → POST /api/chat (message + Authorization: Bearer token)
3. Backend → Verify token (check expiration, signature)
4. Backend → Extract user ID from token
5. Backend → Process request
6. Backend → Return response
```

### Password Security:
- **Never stored plain text** - Always hashed with bcrypt
- **One-way encryption** - Cannot be reversed
- **Salt included** - Each password has unique salt
- **Industry standard** - Same method used by banks

---

## 📡 API Communication

### REST API
- **What it is:** Standard way to communicate between frontend and backend
- **How it works:**
  - Frontend sends HTTP requests (GET, POST)
  - Backend responds with JSON data
  - Example:
    ```
    POST /api/chat
    Headers: Authorization: Bearer token
    Body: { "message": "Create video about Python" }
    Response: { "response": "...", "video_url": "/api/videos/xyz.mp4" }
    ```

### CORS (Cross-Origin Resource Sharing)
- **What it is:** Security feature allowing frontend to call backend
- **Why needed:** Frontend (port 3000) and backend (port 5000) are different origins
- **How it works:** Backend sends headers allowing frontend domain

---

## 🎬 Video Generation Pipeline

### Step-by-Step Process:

1. **User Input:** "Create video about machine learning"
2. **Content Generation (OpenAI):**
   - Generate learning objectives
   - Create slide plan
   - Write scripts for each slide
   - Generate visual descriptions
3. **Visual Generation (Gemini):**
   - Create images for each slide based on descriptions
4. **Audio Generation (OpenAI TTS):**
   - Convert scripts to voiceover audio
5. **Video Assembly (MoviePy):**
   - Combine images, audio, timing
   - Add transitions
   - Export final MP4
6. **Delivery:**
   - Store video file
   - Return URL to frontend
   - User can download or stream

**Total Time:** 2-5 minutes  
**Total Cost:** ~$4 per video

---

## 🔄 Data Flow Example

### Complete User Journey:

```
1. Landing Page (port 3001)
   ↓ User clicks "Coming Soon"
   
2. Login Page (port 3000)
   ↓ User enters credentials
   ↓ Frontend → Backend: POST /api/auth/login
   ↓ Backend → Supabase: Query user
   ↓ Backend → Frontend: Return JWT token
   
3. Dashboard (port 3000)
   ↓ User types: "Create video about Python"
   ↓ Frontend → Backend: POST /api/chat (with token)
   ↓ Backend verifies token
   ↓ Backend → OpenAI: Generate content
   ↓ Backend → Gemini: Generate images
   ↓ Backend → OpenAI TTS: Generate audio
   ↓ Backend → MoviePy: Assemble video
   ↓ Backend → Frontend: Return video URL
   
4. Video Player
   ↓ Displays generated video
   ↓ User can download MP4
```

---

## 💾 Data Storage

### Supabase Tables:

**users:**
- `id` - Unique identifier
- `username` - Login username
- `email` - User email
- `password_hash` - Encrypted password
- `is_active` - Subscription status
- `subscription_expires_at` - When subscription ends
- `created_at` - Account creation date

### File Storage:
- **Videos:** Stored in `backend/output/videos/`
- **Images:** Generated temporarily, used in video
- **Audio:** Generated temporarily, used in video

---

## 🚀 Deployment Architecture

### Development:
- Frontend: `localhost:3000` (Vite dev server)
- Landing: `localhost:3001` (Vite dev server)
- Backend: `localhost:5000` (Uvicorn)

### Production (GitHub Pages):
- Landing: `https://username.github.io/Ampora-AI/`
- Frontend: Can deploy to GitHub Pages or Vercel
- Backend: Deploy to Heroku, Railway, or AWS

---

## 📊 Technology Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend UI | React 18 | User interface |
| Build Tool | Vite | Fast development & builds |
| Routing | React Router | Page navigation |
| Backend API | FastAPI (Python) | API server |
| Database | Supabase (PostgreSQL) | User data storage |
| Authentication | JWT + bcrypt | Secure login |
| Payment | Stripe | Subscription billing |
| AI Content | OpenAI GPT-4 | Text generation |
| AI Images | Google Gemini | Visual generation |
| Video Assembly | MoviePy | Video creation |
| Server | Uvicorn | Runs FastAPI |

---

## 🔒 Security Best Practices

1. **Passwords:** Hashed with bcrypt (one-way encryption)
2. **Tokens:** JWT with expiration (24 hours)
3. **API:** Token required for all protected endpoints
4. **Payment:** Handled by Stripe (PCI compliant)
5. **CORS:** Only allows trusted origins
6. **Environment Variables:** Secrets stored in .env (never committed)

---

## 💡 Why This Stack?

- **React:** Industry standard, large talent pool
- **FastAPI:** Fast, modern, great for AI/ML
- **Supabase:** Free tier, easy setup, scalable
- **Stripe:** Most trusted payment processor
- **OpenAI/Gemini:** Best-in-class AI models

---

This architecture is **production-ready**, **scalable**, and **secure** - perfect for investor presentations!



