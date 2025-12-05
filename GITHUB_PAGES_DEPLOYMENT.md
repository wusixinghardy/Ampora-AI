# GitHub Pages Deployment Guide

This guide explains how to deploy the landing page and frontend app to GitHub Pages.

---

## 📋 Prerequisites

- GitHub repository set up
- Git configured
- All code committed

---

## 🚀 Deploy Landing Page

### Step 1: Install gh-pages

```powershell
cd landing
npm install --save-dev gh-pages
```

### Step 2: Update package.json

Add to `scripts` section:
```json
"scripts": {
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "deploy": "npm run build && gh-pages -d dist"
}
```

### Step 3: Update vite.config.js

Make sure base path is set:
```javascript
export default defineConfig({
  plugins: [react()],
  base: '/Ampora-AI/',  // Your repo name
  // ...
})
```

### Step 4: Deploy

```powershell
npm run deploy
```

### Step 5: Enable GitHub Pages

1. Go to your GitHub repo
2. Settings → Pages
3. Source: `gh-pages` branch
4. Folder: `/ (root)`
5. Save

**Your site will be live at:**
`https://yourusername.github.io/Ampora-AI/`

---

## 🚀 Deploy Frontend App (Optional)

Same process, but deploy to different branch or use different tool:

### Option 1: Separate gh-pages branch
- Deploy to `gh-pages-app` branch
- Access at: `https://yourusername.github.io/Ampora-AI/app/`

### Option 2: Use Vercel/Netlify (Recommended)
- **Vercel:** Connect GitHub repo, auto-deploys
- **Netlify:** Drag & drop dist folder
- Better for React apps with API calls

---

## 🔧 Configuration for Production

### Update API URLs

**Landing page:** No API calls needed

**Frontend app:** Update `.env.production`:
```env
VITE_API_URL=https://your-backend-url.com
```

### Build Commands

**Landing:**
```powershell
cd landing
npm run build
npm run deploy
```

**Frontend:**
```powershell
cd frontend
npm run build
# Then deploy dist/ folder
```

---

## 📝 Important Notes

1. **Base Path:** Must match your repo name in `vite.config.js`
2. **Assets:** All assets must use relative paths
3. **API:** Backend must be deployed separately (Heroku, Railway, AWS)
4. **CORS:** Backend must allow GitHub Pages domain

---

## 🔄 Updating Deployment

After making changes:

```powershell
# Landing page
cd landing
npm run deploy

# Frontend (if using GitHub Pages)
cd frontend
npm run build
# Then deploy dist/ folder
```

---

## 🌐 Custom Domain (Optional)

1. Add `CNAME` file to `gh-pages` branch
2. Content: `yourdomain.com`
3. Update DNS records
4. GitHub Pages will serve from custom domain

---

**Your site will be live and accessible to investors!** 🎉

