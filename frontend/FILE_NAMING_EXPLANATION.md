# File Naming Convention Explanation

This document explains the file naming conventions used in this project.

---

## Current Conventions

### React Components
**Format:** PascalCase (e.g., `ChatInterface.jsx`, `VideoPlayer.jsx`)

**Why:** React convention - component files should match component names exactly.

**Example:**
```jsx
// Component name
const ChatInterface = () => { ... }

// File name matches
ChatInterface.jsx
```

---

### Service/Utility Files
**Format:** lowercase-kebab-case (e.g., `mock-auth.js`, `mock-chat.js`)

**Why:** Clean, readable, follows common Node.js conventions.

---

### CSS Files
**Format:** lowercase-kebab-case (e.g., `chat-interface.css`, `video-player.css`)

**Why:** Matches component names but uses kebab-case (standard for CSS).

---

### Documentation Files
**Format:** UPPERCASE with underscores (e.g., `README.md`, `POSTMAN_GUIDE.md`)

**Why:** 
- Stands out in file listings
- Common convention for important documentation
- Easy to spot at top/bottom of directories

---

### Configuration Files
**Format:** lowercase (e.g., `package.json`, `vite.config.js`, `.env`)

**Why:** Standard tooling conventions.

---

## Why Not All Lowercase?

Some files use mixed case because:
1. **React components** must match component names (PascalCase)
2. **Documentation** benefits from visibility (UPPERCASE)
3. **Consistency** with existing codebase and industry standards

---

## Summary

| File Type | Convention | Example |
|-----------|-----------|---------|
| React Components | PascalCase | `ChatInterface.jsx` |
| Services/Utils | lowercase-kebab | `mock-auth.js` |
| CSS Files | lowercase-kebab | `chat-interface.css` |
| Documentation | UPPERCASE_SNAKE | `README.md` |
| Config Files | lowercase | `package.json` |

**This is intentional and follows industry best practices!**





