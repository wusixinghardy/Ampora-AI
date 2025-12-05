# Troubleshooting Guide

Common issues and their solutions.

---

## 🐛 Issue 1: Black Page / Frontend Won't Load

### Symptoms:
- Browser shows blank/black page
- Console shows errors
- Nothing displays after running `npm run dev`

### Solutions:

1. **Check Browser Console:**
   - Press `F12` to open developer tools
   - Look at "Console" tab for error messages
   - Common errors:
     - `Cannot find module` → Dependencies not installed
     - `Failed to load resource` → Missing files

2. **Clear Browser Cache:**
   - Press `Ctrl + Shift + Delete`
   - Clear cached images and files
   - Refresh page

3. **Restart Dev Server:**
   ```powershell
   # Stop server (Ctrl + C)
   # Then restart:
   npm run dev
   ```

4. **Reinstall Dependencies:**
   ```powershell
   Remove-Item -Recurse -Force node_modules
   npm install
   npm run dev
   ```

5. **Check for JavaScript Errors:**
   - Open browser console (F12)
   - Look for red error messages
   - Share error with developer

---

## 🐛 Issue 2: Postman Error "ECONNREFUSED 127.0.0.1:5000"

### What This Means:
- **The backend server is NOT running** on port 5000
- This is **EXPECTED** because the backend hasn't been implemented yet

### Why It Happens:
```
Error: connect ECONNREFUSED 127.0.0.1:5000
```

This error means Postman tried to connect to `http://localhost:5000` but found nothing there.

### Solutions:

**Option 1: Wait for Backend (Recommended)**
- The backend needs to be implemented first
- Once Hardy/Sam creates the backend:
  1. Start backend server on port 5000
  2. Then Postman will work

**Option 2: Use Mock Services (Current Setup)**
- Frontend uses mock services that work in browser
- Test authentication/login in the browser UI
- Mock services don't work via Postman (they're browser-based)

**Option 3: Check Backend Status**
- Ask teammates if backend is ready
- Check if backend server is running:
  ```powershell
  # Check if port 5000 is in use:
  netstat -ano | findstr :5000
  ```

### When Will Postman Work?
Postman will work once:
1. ✅ Backend is implemented
2. ✅ Backend server is running
3. ✅ Server is listening on port 5000

---

## 🐛 Issue 3: Port 3000 Already in Use

### Error:
```
Port 3000 is already in use
```

### Solution:
1. **Find what's using port 3000:**
   ```powershell
   netstat -ano | findstr :3000
   ```
2. **Kill the process** or change port in `vite.config.js`

3. **Or change port:**
   - Edit `vite.config.js`
   - Change `port: 3000` to `port: 3001`

---

## 🐛 Issue 4: Module Not Found Errors

### Error:
```
Cannot find module 'react-router-dom'
```

### Solution:
```powershell
npm install
```

If that doesn't work:
```powershell
Remove-Item -Recurse -Force node_modules
npm cache clean --force
npm install
```

---

## 🐛 Issue 5: Login Not Working

### Check:
1. **Using correct test account?**
   - Username: `testuser`
   - Password: `test123`

2. **Browser console errors?**
   - Press F12 → Console tab
   - Look for red errors

3. **Mock auth enabled?**
   - Check `src/services/mockAuth.js`
   - Should have `USE_MOCK_AUTH = true`

---

## 🐛 Issue 6: CSS Not Loading

### Solutions:
1. **Hard refresh browser:**
   - `Ctrl + Shift + R` or `Ctrl + F5`

2. **Clear browser cache**

3. **Check file paths:**
   - CSS imports should use relative paths
   - Example: `'../styles/LoginSignup.css'`

---

## 🔍 Debugging Tips

### 1. Check Browser Console
- Press `F12`
- Look at Console, Network, and Elements tabs
- Errors usually show in red

### 2. Check Terminal Output
- Look at the terminal running `npm run dev`
- Errors will show there too

### 3. Verify File Structure
- Make sure all files exist
- Check import paths are correct
- Verify component names match file names

### 4. Test in Different Browser
- Try Chrome, Edge, or Firefox
- Rule out browser-specific issues

---

## ✅ Still Having Issues?

1. **Check all error messages** in browser console
2. **Share specific error text** with developer
3. **Note what you were doing** when error occurred
4. **Screenshot** the error if possible

---

## 📞 Getting Help

For backend issues: Ask Hardy/Sam  
For frontend issues: Check this guide first, then ask for help with specific error messages.



