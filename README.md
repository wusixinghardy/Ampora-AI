# Ampora AI - AI-Powered Career Learning Platform

Transform any technical concept into a complete video lesson with slides, voiceover, and visual explanations—generated in minutes, not hours.

---

## 🚀 Quick Start

**See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for complete setup instructions.**

### 3-Minute Setup:

1. **Backend:**
   ```powershell
   cd backend
   python -m venv venv-fastapi
   venv-fastapi\Scripts\activate
   pip install -r requirements.txt
   # Create .env file (see SETUP_GUIDE.md)
   python main.py
   ```

2. **Frontend:**
   ```powershell
   cd frontend
   npm install
   # Create .env file (see SETUP_GUIDE.md)
   npm run dev
   ```

3. **Landing Page:**
   ```powershell
   cd landing
   npm install
   npm run dev
   ```

**Access:**
- Landing: http://localhost:3001
- App: http://localhost:3000
- API: http://localhost:5000

---

## 📁 Project Structure

```
Ampora-AI/
├── artifacts/              # Demo videos, logos, team photos
├── backend/                # FastAPI server (Python)
│   ├── main.py            # API endpoints
│   ├── src/               # Services (video, voice, visualization)
│   └── requirements.txt   # Python dependencies
├── frontend/              # Main application (React)
│   ├── src/
│   │   ├── components/   # UI components
│   │   └── services/     # API services
│   └── package.json
├── landing/               # Marketing website (React)
│   ├── src/
│   └── package.json
└── [documentation files]
```

---

## 🎯 Features

- ✅ **AI Video Generation** - Create complete video lessons from text prompts
- ✅ **User Authentication** - Secure login/signup with Supabase
- ✅ **Payment Integration** - Stripe monthly subscriptions
- ✅ **Landing Page** - Professional marketing site
- ✅ **Chat Interface** - Interactive chatbot for video requests
- ✅ **Video Player** - Download and view generated videos

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](./SETUP_GUIDE.md) | Complete setup instructions |
| [TECHNOLOGY_EXPLANATION.md](./TECHNOLOGY_EXPLANATION.md) | Tech stack explained (for investors) |
| [COMPLETE_IMPLEMENTATION_SUMMARY.md](./COMPLETE_IMPLEMENTATION_SUMMARY.md) | What was built and next steps |
| [ACCESSING_PAGES_GUIDE.md](./ACCESSING_PAGES_GUIDE.md) | How to access all 3 pages for recording |
| [GITHUB_PAGES_DEPLOYMENT.md](./GITHUB_PAGES_DEPLOYMENT.md) | Deploy to GitHub Pages |
| [frontend/POSTMAN_GUIDE.md](./frontend/POSTMAN_GUIDE.md) | API testing with Postman |

---

## 🔧 Configuration Required

### Backend (.env)
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
STRIPE_SECRET_KEY=sk_test_...
STRIPE_SUBSCRIPTION_PRICE=9.99
JWT_SECRET=your-secret-key
TEST_MODE=true
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
VITE_USE_MOCK_AUTH=false
VITE_USE_MOCK_CHAT=false
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

---

## 🧪 Test Accounts

These accounts bypass payment (for development):
- `testuser` / `test123`
- `demo` / `demo123`
- `dev` / (any password)
- `admin` / (any password)

---

## 💰 Pricing

- **Subscription:** $9.99/month (configurable)
- **Video Generation:** ~$4 per video (AI API costs)
- **Change Price:** Edit `STRIPE_SUBSCRIPTION_PRICE` in backend .env

---

## 🛠️ Tech Stack

- **Frontend:** React 18, Vite, React Router
- **Backend:** FastAPI (Python), Uvicorn
- **Database:** Supabase (PostgreSQL)
- **Authentication:** JWT, bcrypt
- **Payment:** Stripe
- **AI:** OpenAI GPT-4, Google Gemini
- **Video:** MoviePy

**See [TECHNOLOGY_EXPLANATION.md](./TECHNOLOGY_EXPLANATION.md) for details.**

---

## 📝 Next Steps

1. ✅ Set up Supabase (create users table)
2. ✅ Set up Stripe (get API keys)
3. ✅ Configure .env files
4. ✅ Add team photos to artifacts/
5. ✅ Add Google Forms link
6. ✅ Record demo video
7. ✅ Deploy to GitHub Pages

**See [COMPLETE_IMPLEMENTATION_SUMMARY.md](./COMPLETE_IMPLEMENTATION_SUMMARY.md) for checklist.**

---

## 🎬 For Investors

**Key Highlights:**
- Modern, scalable architecture
- Production-ready code
- Secure authentication & payments
- AI-powered content generation
- Professional landing page

**Demo:**
- Landing page: http://localhost:3001
- App: http://localhost:3000
- Test account: `testuser` / `test123`

---

## 📞 Support

For setup issues, see [SETUP_GUIDE.md](./SETUP_GUIDE.md).  
For technology questions, see [TECHNOLOGY_EXPLANATION.md](./TECHNOLOGY_EXPLANATION.md).

---

**Built with ❤️ by the Ampora AI Team**
