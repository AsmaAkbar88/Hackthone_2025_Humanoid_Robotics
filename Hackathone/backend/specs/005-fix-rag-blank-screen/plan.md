# Implementation Plan: Fix RAG Book App Blank Screen

**Feature Branch**: `005-fix-rag-blank-screen`
**Created**: 2026-01-01
**Status**: Ready for Implementation
**Spec**: `specs/005-fix-rag-blank-screen/spec.md`

---

## Technical Context

### Known Issues (from spec)

1. **clientModules.js** - Duplicate `export default` causing module conflicts
2. **clientModules.js** - Invalid path `../backend/ui_chatbot/components/ChatWidget`
3. **ChatWidget.jsx** - CSS import path mismatch (`./chatWidget.css`)
4. **src/css/chatbot.css** - Empty/minimal styles
5. **plugin-chatbot.js** - CSS not properly linked

### Files to Modify

| File | Issue | Fix |
|------|-------|-----|
| `book-docusaurus/src/clientModules.js` | Duplicate export, invalid import | Remove duplicate, fix path |
| `book-docusaurus/src/components/chatbot/ChatWidget.jsx` | CSS import wrong | Fix relative path |
| `book-docusaurus/src/css/chatbot.css` | Empty | Add CSS styles |
| `book-docusaurus/src/plugin-chatbot.js` | Static CSS not linked | Verify link |

---

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| Zero Hallucination | ✅ N/A | This is a frontend bug fix, not RAG response generation |
| Context Isolation | ✅ N/A | No context changes |
| Spec-First Determinism | ✅ N/A | Following spec exactly |
| Hackathon Simplicity | ✅ N/A | Minimal focused changes |
| Free-Tier Compatibility | ✅ N/A | No service changes |

---

## Implementation Steps

### Phase 1: Fix clientModules.js

**File**: `book-docusaurus/src/clientModules.js`

**Problems**:
- Duplicate `export default function` definitions
- Invalid dynamic import path to backend

**Steps**:
1. Read current file
2. Remove duplicate export
3. Fix import path from `../backend/ui_chatbot/components/ChatWidget` to `./components/chatbot/ChatWidget`

### Phase 2: Fix ChatWidget CSS import

**File**: `book-docusaurus/src/components/chatbot/ChatWidget.jsx`

**Problem**:
- Import path `./chatWidget.css` doesn't match actual file location

**Steps**:
1. Read current file
2. Identify CSS import
3. Fix path to `../../css/chatbot.css`

### Phase 3: Add chatbot CSS styles

**File**: `book-docusaurus/src/css/chatbot.css`

**Problem**:
- File is empty/minimal (only contains `#chatbot-widget-root` placeholder)

**Steps**:
1. Read static/css/chatbot.css to get full styles
2. Copy styles to src/css/chatbot.css
3. Remove/keep minimal version in static/css/chatbot.css

### Phase 4: Verify plugin CSS linking

**File**: `book-docusaurus/src/plugin-chatbot.js`

**Problem**:
- Static CSS may not be properly linked

**Steps**:
1. Read current file
2. Verify href path `/css/chatbot.css` is correct
3. Verify static/css/chatbot.css exists

---

## Files Reference

### Existing Files (modify only)

```
book-docusaurus/src/
├── clientModules.js              # Fix duplicate export + import path
├── components/chatbot/
│   └── ChatWidget.jsx           # Fix CSS import path
├── css/
│   └── chatbot.css              # Add missing styles
└── plugin-chatbot.js            # Verify CSS linking

book-docusaurus/static/css/
└── chatbot.css                   # Reference for styles
```

### Output Files (create if needed)

None - working only with existing files

---

## Success Verification

1. Run `npm run build` in book-docusaurus - should complete without errors
2. Homepage renders with title and content
3. Chatbot floating button visible in bottom-right
4. No JavaScript console errors on page load

---

## Out of Scope (per spec)

- Backend API changes
- Qdrant configuration
- RAG embedding pipeline
- Production deployment
