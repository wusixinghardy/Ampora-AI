# Ampora AI Frontend

Modern React-based frontend for Ampora AI, featuring authentication, chatbot interface, and video generation.

## Quick Start

### Prerequisites
- Node.js (v18 or higher) - [Download](https://nodejs.org/)
- npm (comes with Node.js)

### Installation & Run

1. Navigate to frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start development server:
```powershell
npm run dev
```

4. Open browser:
```
http://localhost:3000
```

---

## Features

- ✅ **Authentication** - Login and Signup with mock auth (backend-ready)
- ✅ **Chat Interface** - Interactive chatbot with mock responses
- ✅ **Loading Indicator** - Real-time backend processing status
- ✅ **Video Player** - Display and download generated videos
- ✅ **Responsive Design** - Works on desktop and mobile

---

## Test Accounts

The frontend uses **mock authentication** for testing without backend. Use these test accounts to log in:

| Username | Password | Email |
|----------|----------|-------|
| `testuser` | `test123` | test@example.com |
| `demo` | `demo123` | demo@example.com |

**How to Use:**
1. Open login page
2. Enter one of the credentials above
3. Click Login → You'll be redirected to dashboard!

**Note:** These accounts are stored in browser localStorage for testing. You can also create new accounts via Sign Up tab. All test accounts persist until browser data is cleared.

**To switch to real backend:** Set `VITE_USE_MOCK_AUTH=false` in `.env` file.

---

## Sample Chatbot Prompts

Copy and paste these prompts into the chat interface to test:

### Video Generation
```
Create a video about machine learning basics
Generate a video explaining Python programming
Make a video tutorial on React hooks
I need a video about data science fundamentals
```

### Lecture Generation
```
Create a lecture video about quantum computing
Generate a lecture on artificial intelligence history
Make an educational video about neural networks
I want a lecture video on web development best practices
```

### Specific Topics
```
Generate a video explaining how HTTP works
Create a video about database design principles
Make a tutorial video on REST API development
I need a video about cloud computing architecture
```

### General Testing
```
Hello
Help
What can you do?
```

### Detailed Requests
```
Create a 10-minute video lecture about machine learning algorithms with visualizations
Generate an educational video about Python for beginners, make it engaging and fun
Make a video explaining React state management with code examples
I need a comprehensive video about data structures and algorithms
```

**Tips for Better Results:**
- Be specific about topic and audience
- Mention preferred video length
- Request specific features (animations, code examples, etc.)

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx      # Chatbot component
│   │   ├── Dashboard.jsx          # Main dashboard layout
│   │   ├── LoadingIndicator.jsx   # Loading animation
│   │   ├── LoginSignup.jsx        # Authentication
│   │   ├── VideoPlayer.jsx        # Video display & download
│   │   └── WaveIcon.jsx           # Wavelength icon
│   ├── services/
│   │   ├── mockAuth.js            # Mock authentication
│   │   └── mockChat.js            # Mock chat service
│   ├── styles/                    # Component CSS files
│   ├── App.jsx                    # Main app with routing
│   └── main.jsx                   # React entry point
├── public/
│   └── ampora_ai_logo.png         # Logo & favicon
├── index.html
├── package.json
└── vite.config.js
```

---

## Backend Integration

### Current Status: Mock Mode

The frontend uses mock services for testing without backend:
- Mock authentication (`src/services/mockAuth.js`)
- Mock chat service (`src/services/mockChat.js`)

### Switching to Real Backend

When backend is ready, set environment variables:

```bash
# .env file
VITE_USE_MOCK_AUTH=false
VITE_USE_MOCK_CHAT=false
VITE_API_URL=http://localhost:5000
```

Or modify in code:
- `src/services/mockAuth.js` - Set `USE_MOCK_AUTH = false`
- `src/services/mockChat.js` - Set `USE_MOCK_CHAT = false`

### Expected Backend Endpoints

```
POST /api/auth/login
  Body: { username, password }
  Response: { token, user }

POST /api/auth/signup
  Body: { username, email, password }
  Response: { token, user }

POST /api/chat
  Headers: Authorization: Bearer {token}
  Body: { message }
  Response: { response, video_url? }
```

---

## Environment Variables

Create `.env` file in frontend directory:

```env
# Backend API URL
VITE_API_URL=http://localhost:5000

# Mock services (set to false when backend ready)
VITE_USE_MOCK_AUTH=true
VITE_USE_MOCK_CHAT=true
```

---

## Technologies

- **React 18** - UI framework
- **React Router DOM** - Routing
- **Vite** - Build tool
- **React Icons** - Icons

---

## Troubleshooting

### Port Already in Use
Change port in `vite.config.js` or stop other services on port 3000.

### Dependencies Not Installing
```powershell
Remove-Item -Recurse -Force node_modules
npm cache clean --force
npm install
```

### Module Not Found Errors
Restart dev server after installing new dependencies.

---

## File Naming Convention

**Component Files:** Use PascalCase (e.g., `ChatInterface.jsx`) - This follows React conventions where component files match component names.

**Other Files:** Use lowercase with hyphens or camelCase:
- ✅ `mock-auth.js` - Service files
- ✅ `video-player.css` - CSS files
- ✅ `POSTMAN_GUIDE.md` - Documentation (UPPERCASE for emphasis)

**Why this mix?**
- React components use PascalCase to match component names
- Utilities/services use lowercase-kebab-case for consistency
- Documentation files use UPPERCASE to stand out in file listings
- This matches common industry conventions

---

## Testing with Postman

See `POSTMAN_GUIDE.md` for API endpoint testing instructions.

---

## Future Features

- ⏳ Stripe payment integration (see `STRIPE_INTEGRATION_NOTES.md`)
- ⏳ Real-time video generation status
- ⏳ User profile management
- ⏳ Video history

---

## Development

### Build for Production
```powershell
npm run build
```

### Preview Production Build
```powershell
npm run preview
```

---

For more details, see the root `README.md` in the Ampora-AI folder.