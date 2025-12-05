# How to Access All 3 Pages for Recording

This guide explains how to access the landing page, login page, and chatbot page separately for recording your demo video.

---

## 🎬 Why You Need This

The landing page's "Coming Soon" button doesn't link to the app yet (by design). To record the demo, you need to access all 3 pages separately.

---

## 📍 Page URLs

### 1. Landing Page
**URL:** `http://localhost:3001`  
**What it shows:** Marketing site with team profiles, demo videos, Google Forms link

### 2. Login/Signup Page
**URL:** `http://localhost:3000/login`  
**What it shows:** Authentication form (login and signup tabs)

### 3. Chatbot/Dashboard Page
**URL:** `http://localhost:3000/dashboard`  
**What it shows:** Chat interface, loading indicator, video player  
**Note:** Requires login first (redirects to /login if not authenticated)

---

## 🚀 Step-by-Step: Starting All Pages

### Terminal 1: Backend Server
```powershell
cd backend
venv-fastapi\Scripts\activate
python main.py
```
**Wait for:** `Uvicorn running on http://0.0.0.0:5000`

### Terminal 2: Frontend App (Login/Chat)
```powershell
cd frontend
npm run dev
```
**Wait for:** `Local: http://localhost:3000/`

### Terminal 3: Landing Page
```powershell
cd landing
npm run dev
```
**Wait for:** `Local: http://localhost:3001/`

---

## 🎥 Recording Workflow

### Option 1: Record All in One Flow

1. **Start all 3 servers** (see above)

2. **Open browser tabs:**
   - Tab 1: `http://localhost:3001` (Landing page)
   - Tab 2: `http://localhost:3000/login` (Login page)
   - Tab 3: `http://localhost:3000/dashboard` (Will redirect to login if not logged in)

3. **Start screen recording**

4. **Show landing page:**
   - Scroll through sections
   - Show team profiles
   - Show demo videos
   - Click "Get Free Trial Access" button

5. **Switch to login tab:**
   - Show login form
   - Enter test credentials: `testuser` / `test123`
   - Click Login

6. **Show dashboard:**
   - Chat interface on left
   - Loading indicator on right
   - Video player at bottom

7. **Demonstrate chat:**
   - Type: "Create a video about Python basics"
   - Show loading indicator spinning
   - Show response
   - Show video appearing (if generated)

8. **Stop recording**

### Option 2: Record Separately Then Edit

1. **Record landing page separately** (just landing page)
2. **Record app flow separately** (login → chat → video)
3. **Edit together** in video editor

---

## 🔑 Test Credentials

Use these to login without payment:
- **Username:** `testuser`
- **Password:** `test123`

Or:
- **Username:** `demo`
- **Password:** `demo123`

---

## 📝 Recording Tips

1. **Full Screen:** Record in full screen for best quality
2. **Resolution:** Record at 1080p or higher
3. **Frame Rate:** 30fps is fine, 60fps is better
4. **Audio:** Narrate what you're doing
5. **Pacing:** Go slowly, let viewers see each step
6. **Highlights:** 
   - Show the AI generating content
   - Show loading states
   - Show final video result

---

## 🎬 What to Show in Recording

### Landing Page Section:
- ✅ Hero section with logo
- ✅ About section explaining the product
- ✅ Demo videos (bubble sort + your recording)
- ✅ Team profiles
- ✅ Call-to-action buttons

### App Section:
- ✅ Login page design
- ✅ Signup form (mention Stripe payment)
- ✅ Dashboard layout
- ✅ Chat interface
- ✅ Loading indicator animation
- ✅ Video generation process
- ✅ Video player with download

---

## 💾 Save Your Recording

1. **Save as:** `screen_recording_demo.mp4`
2. **Location:** `artifacts/screen_recording_demo.mp4`
3. **Update Demos component:** The placeholder will automatically show your video once saved

---

## 🔄 After Recording

1. **Save video** to `artifacts/screen_recording_demo.mp4`
2. **Update Demos.jsx** (if needed) to use the new filename
3. **Test playback** on landing page
4. **Ready for investors!** 🎉

---

## ⚠️ Troubleshooting

**Can't access pages:**
- Check all 3 servers are running
- Check ports aren't blocked by firewall
- Try refreshing browser

**Login doesn't work:**
- Check backend is running
- Check Supabase is configured
- Use test accounts to bypass payment

**Video doesn't generate:**
- Check OpenAI API key in backend .env
- Check backend logs for errors
- Video generation takes 2-5 minutes

---

**You're all set! Start recording when ready.** 🎥

