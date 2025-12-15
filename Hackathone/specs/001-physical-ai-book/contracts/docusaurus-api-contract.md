# Docusaurus API Contract: book-physical-ai

## Overview
This document defines the API contracts for the book-physical-ai Docusaurus project. Since this is a static documentation site, the "API" refers to the content structure and data contracts used by the Docusaurus framework.

## Content API

### Module Content Structure
```
GET /api/modules/{moduleId}
```

**Response:**
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "pages": [
    {
      "id": "string",
      "title": "string",
      "path": "string",
      "order": "number"
    }
  ],
  "prerequisites": ["string"],
  "learningObjectives": ["string"]
}
```

### Page Content Structure
```
GET /api/pages/{pageId}
```

**Response:**
```json
{
  "id": "string",
  "title": "string",
  "content": "markdown string",
  "module": "string",
  "navigationOrder": "number",
  "relatedPages": [
    {
      "id": "string",
      "title": "string",
      "path": "string"
    }
  ]
}
```

### Search API
```
GET /api/search?q={query}&limit={number}
```

**Response:**
```json
{
  "query": "string",
  "results": [
    {
      "id": "string",
      "title": "string",
      "path": "string",
      "excerpt": "string",
      "score": "number"
    }
  ],
  "total": "number"
}
```

## Navigation Contract

### Sidebar Structure
The sidebar.js file must export a structure that follows this contract:

```javascript
module.exports = {
  module1: [
    {
      type: 'doc',
      id: 'module-1-ros2/index',
      label: 'ROS 2 Fundamentals'
    },
    {
      type: 'doc',
      id: 'module-1-ros2/basics',
      label: 'Basics'
    }
    // ... more pages
  ],
  module2: [
    // ... similar structure for other modules
  ]
};
```

## Static Asset Contract

### Image Requirements
- Format: PNG, JPG, GIF, SVG, WebP
- Size: Optimized for web (max 2MB per image)
- Dimensions: Responsive and optimized for different screen sizes
- Location: `/static/img/` directory

### Document Requirements
- Format: PDF for downloadable resources
- Location: `/static/docs/` directory
- Size: Optimized for web download

## Build Contract

### Configuration Requirements
The `docusaurus.config.js` file must include:

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Comprehensive Guide to Physical AI Systems',
  url: 'https://your-domain.github.io',
  baseUrl: '/book-physical-ai/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  // ... other required configuration
};
```

## Deployment Contract

### GitHub Pages Deployment
- Source branch: `main`
- Build output: `build/` directory
- Deployment path: Root of GitHub Pages site
- Custom domain: Optional via CNAME file