# Postman API Testing Guide

This guide explains how to use Postman to test the Ampora AI backend API endpoints.

---

## 🚀 Why Use Postman?

Postman allows you to:
- Test API endpoints without the frontend
- Debug backend responses
- Test authentication flows
- Verify video generation endpoints
- Share API documentation with teammates

---

## 📥 Installing Postman

1. **Download Postman:**
   - Go to [postman.com/downloads](https://www.postman.com/downloads)
   - Download for Windows
   - Install the application

2. **Create Account (Optional but Recommended):**
   - Free account allows syncing across devices
   - Not required for basic testing

---

## ⚠️ Important: Backend Must Be Running!

**The error "ECONNREFUSED 127.0.0.1:5000" means:**
- No server is running on port 5000
- The backend hasn't been implemented yet OR
- The backend server is not started

**You CANNOT test backend endpoints with Postman until:**
1. The backend is implemented by Hardy/Sam
2. The backend server is running on port 5000

**Current Status:**
- ✅ Frontend uses **mock services** (works without backend)
- ❌ **No real backend yet** - Postman won't work until backend is ready
- ⏳ Postman testing will work once backend is running

---

## 🧪 Testing Mock Endpoints (Current Frontend)

Since the frontend uses mock services, you can test them via localStorage or directly in browser console. However, once the backend is ready, use Postman to test:

---

## 📋 Setting Up Postman

### 1. Create a New Collection

1. Open Postman
2. Click **"New"** → **"Collection"**
3. Name it: `Ampora AI API`

### 2. Set Collection Variables

1. Click on your collection
2. Go to **"Variables"** tab
3. Add these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:5000` | `http://localhost:5000` |
| `token` | (leave empty) | (will be set after login) |

---

## 🔐 Authentication Endpoints

### Test 1: User Login

**Request Setup:**
- Method: `POST`
- URL: `{{base_url}}/api/auth/login`
- Headers:
  ```
  Content-Type: application/json
  ```
- Body (raw JSON):
  ```json
  {
    "username": "testuser",
    "password": "test123"
  }
  ```

**Expected Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_123",
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**After Success:**
- Copy the `token` value
- In Collection Variables, set `token` variable to this value

---

### Test 2: User Signup

**Request Setup:**
- Method: `POST`
- URL: `{{base_url}}/api/auth/signup`
- Headers:
  ```
  Content-Type: application/json
  ```
- Body (raw JSON):
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123"
  }
  ```

**Expected Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_456",
    "username": "newuser",
    "email": "newuser@example.com"
  }
}
```

---

## 💬 Chat Endpoints

### Test 3: Send Chat Message

**Request Setup:**
- Method: `POST`
- URL: `{{base_url}}/api/chat`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer {{token}}
  ```
- Body (raw JSON):
  ```json
  {
    "message": "Create a video about machine learning"
  }
  ```

**Expected Response:**
```json
{
  "response": "I'm processing your video generation request...",
  "video_url": null
}
```

**Or with Video:**
```json
{
  "response": "Your video has been generated!",
  "video_url": "http://localhost:5000/videos/generated_video_123.mp4"
}
```

---

## 🎬 Video Generation Endpoints

### Test 4: Get Video Status

(When implemented by backend team)

**Request Setup:**
- Method: `GET`
- URL: `{{base_url}}/api/video/status/{video_id}`
- Headers:
  ```
  Authorization: Bearer {{token}}
  ```

---

## 🔧 Postman Tips

### Using Environment Variables

1. Click **"Environments"** in left sidebar
2. Create new environment: `Ampora AI Local`
3. Add variables:
   - `base_url` = `http://localhost:5000`
   - `token` = (leave empty, set after login)
4. Select this environment in top-right dropdown

### Automating Token Setting

1. In Login request, go to **"Tests"** tab
2. Add this script:
   ```javascript
   if (pm.response.code === 200) {
       var jsonData = pm.response.json();
       pm.environment.set("token", jsonData.token);
       console.log("Token saved to environment");
   }
   ```
3. Now token auto-updates after login!

### Testing Different Environments

Create multiple environments:
- `Local` - `http://localhost:5000`
- `Development` - `https://dev-api.ampora-ai.com`
- `Production` - `https://api.ampora-ai.com`

Switch between them easily!

---

## 📤 Exporting/Importing Collections

### Export Collection:
1. Click collection → **"..."** → **"Export"**
2. Save as JSON file
3. Share with teammates

### Import Collection:
1. Click **"Import"** button
2. Select JSON file
3. Collection appears in sidebar

---

## 🐛 Common Issues

### "Network Error"
- Check if backend server is running
- Verify `base_url` is correct
- Check firewall/antivirus

### "401 Unauthorized"
- Token expired or invalid
- Re-run login request to get new token
- Check Authorization header format

### "CORS Error"
- Backend needs CORS headers configured
- Contact backend team

---

## 📝 Example Workflow

1. **Start Backend Server** (when ready)
2. **Open Postman**
3. **Login Request** → Get token
4. **Set Token** in environment variables
5. **Send Chat Message** → Test chat endpoint
6. **Check Response** → Verify format
7. **Test Video Generation** → When implemented

---

## 🔗 Useful Resources

- [Postman Learning Center](https://learning.postman.com/)
- [Postman Documentation](https://www.postman.com/api-documentation-tool/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Note:** These endpoints will be available once the backend is implemented by Hardy and Sam. Use this guide to test when backend is ready!
