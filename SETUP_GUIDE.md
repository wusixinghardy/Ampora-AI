# Complete Setup Guide - Ampora AI

This guide covers all setup steps for the full Ampora AI platform.

---

## 📋 Overview

The project consists of:
1. **Landing Page** - Marketing site (port 3001)
2. **Frontend App** - Main application with login/chat (port 3000)
3. **Backend API** - FastAPI server (port 5000)

---

## 🚀 Quick Start

### 1. Backend Setup

```powershell
cd backend

# Create virtual environment
python -m venv venv-fastapi
venv-fastapi\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example and fill in your keys
```

**Backend .env file needed:**
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SUBSCRIPTION_PRICE=9.99
JWT_SECRET=your-secret-key-change-this
TEST_MODE=true
TEST_MODE_NO_DB=true  # set true to allow test accounts without Supabase in dev
```

**Start backend:**
```powershell
python main.py
# Or: uvicorn main:app --reload --port 5000
```

### 2. Frontend Setup (Main App)

```powershell
cd frontend

# Install dependencies
npm install

# Create .env file
# VITE_API_URL=http://localhost:5000
# VITE_USE_MOCK_AUTH=false
# VITE_USE_MOCK_CHAT=false
# VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Start frontend
npm run dev
```

### 3. Landing Page Setup

```powershell
cd landing

# Install dependencies
npm install

# Start landing page
npm run dev
```

---

## 🔐 Supabase Setup

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Note your project URL and anon key

### Step 2: Create Users Table

In Supabase SQL Editor, run:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  is_active BOOLEAN DEFAULT true,
  subscription_expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for faster lookups
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

### Step 3: Add to Backend .env

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here
```

---

## 💳 Stripe Setup

### Step 1: Create Stripe Account

1. Go to [stripe.com](https://stripe.com)
2. Create account (use test mode for development)
3. Get API keys from Dashboard → Developers → API keys

### Step 2: Create Subscription Product

1. Go to Products → Add Product
2. Create monthly subscription:
   - Name: "Ampora AI Monthly Subscription"
   - Price: $9.99/month (or your price)
   - Billing: Monthly
3. Note the Price ID (starts with `price_`)

### Step 3: Add Keys to .env

**Backend .env:**
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_SUBSCRIPTION_PRICE=9.99
```

**Frontend .env:**
```env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Step 4: Change Subscription Price

Edit `backend/main.py`:
```python
STRIPE_SUBSCRIPTION_PRICE = os.getenv("STRIPE_SUBSCRIPTION_PRICE", "9.99")
```

Or set in `.env`:
```env
STRIPE_SUBSCRIPTION_PRICE=19.99  # Change to your price
```

---

## 🧪 Test Accounts (Bypass Payment)

Test accounts that bypass Stripe payment:
- `testuser`
- `demo`
- `dev`
- `admin`

Add more in `backend/main.py`:
```python
TEST_ACCOUNTS = ["testuser", "demo", "dev", "admin", "your-test-account"]
```

---

## 📱 Running All 3 Pages

### For Development/Recording:

1. **Terminal 1 - Backend:**
   ```powershell
   cd backend
   venv-fastapi\Scripts\activate
   python main.py
   ```

2. **Terminal 2 - Frontend App:**
   ```powershell
   cd frontend
   npm run dev
   # Access at: http://localhost:3000
   ```

3. **Terminal 3 - Landing Page:**
   ```powershell
   cd landing
   npm run dev
   # Access at: http://localhost:3001
   ```

### Access URLs:
- **Landing Page:** http://localhost:3001
- **Login/Signup:** http://localhost:3000/login
- **Dashboard/Chat:** http://localhost:3000/dashboard (after login)

---

## 🎬 Recording the Demo Video

To record the screen recording demo:

1. **Start all 3 servers** (see above)
2. **Open landing page:** http://localhost:3001
3. **Open frontend in new tab:** http://localhost:3000
4. **Login with test account:** `testuser` / `test123`
5. **Record your screen** showing:
   - Landing page overview
   - Navigating to login
   - Logging in
   - Using the chat to generate a video
   - Video appearing in player
6. **Save video** to `artifacts/screen_recording_demo.mp4`

---

## 📝 Postman Usage

### Setup:

1. **Install Postman** from [postman.com](https://postman.com)

2. **Create Collection:**
   - New → Collection → Name: "Ampora AI API"

3. **Set Variables:**
   - Collection → Variables tab:
     - `base_url` = `http://localhost:5000`
     - `token` = (leave empty, auto-filled after login)

### Test Endpoints:

**1. Health Check:**
- GET `{{base_url}}/api/health`

**2. Login:**
- POST `{{base_url}}/api/auth/login`
- Body (JSON):
  ```json
  {
    "username": "testuser",
    "password": "test123"
  }
  ```
- In "Tests" tab, add:
  ```javascript
  if (pm.response.code === 200) {
      var jsonData = pm.response.json();
      pm.collectionVariables.set("token", jsonData.token);
  }
  ```

**3. Chat:**
- POST `{{base_url}}/api/chat`
- Headers: `Authorization: Bearer {{token}}`
- Body (JSON):
  ```json
  {
    "message": "Create a video about machine learning"
  }
  ```

**4. Get Video:**
- GET `{{base_url}}/api/videos/{filename}`

---

## 🚀 GitHub Pages Deployment

### Landing Page Deployment:

1. **Build landing page:**
   ```powershell
   cd landing
   npm run build
   ```

2. **Install gh-pages:**
   ```powershell
   npm install --save-dev gh-pages
   ```

3. **Add to package.json scripts:**
   ```json
   "scripts": {
     "deploy": "npm run build && gh-pages -d dist"
   }
   ```

4. **Deploy:**
   ```powershell
   npm run deploy
   ```

5. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: `gh-pages` branch
   - Your site: `https://username.github.io/Ampora-AI/`

### Frontend App Deployment:

Same process, but deploy to different branch or subdirectory.

---

## 🔧 Configuration Files

### Backend .env Template:
```env
# AI Services
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
MODEL_NAME=gpt-4o

# Database
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx

# Payment
STRIPE_SECRET_KEY=sk_test_...
STRIPE_SUBSCRIPTION_PRICE=9.99

# Security
JWT_SECRET=change-this-to-random-string

# Development
TEST_MODE=true
```

### Frontend .env Template:
```env
VITE_API_URL=http://localhost:5000
VITE_USE_MOCK_AUTH=false
VITE_USE_MOCK_CHAT=false
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

---

## 📚 Technology Stack Explained

See `TECHNOLOGY_EXPLANATION.md` for detailed explanations.

---

## ❓ Troubleshooting

### Backend won't start:
- Check Python version (3.8+)
- Activate virtual environment
- Install all requirements
- Check .env file exists

### Frontend can't connect:
- Check backend is running on port 5000
- Check CORS settings in backend
- Verify VITE_API_URL in frontend .env

### Supabase errors:
- Verify URL and key in .env
- Check table exists in Supabase
- Verify RLS policies allow access

### Stripe errors:
- Use test keys for development
- Check price ID is correct
- Verify webhook endpoints if using

---

For more details, see individual component README files.

