# Quickstart Guide: book-physical-ai

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Basic knowledge of Markdown syntax

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [repository-url]
cd book-physical-ai
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Start Development Server
```bash
npm start
# or
yarn start
```

This will start a local development server at `http://localhost:3000` with hot reloading.

### 4. Build for Production
```bash
npm run build
# or
yarn build
```

## Project Structure Overview

```
book-physical-ai/
├── docs/                 # Content files
│   ├── module-1-ros2/    # ROS 2 module content
│   ├── module-2-gazebo/  # Gazebo/Unity module content
│   ├── module-3-nvidia-isaac/ # NVIDIA Isaac module content
│   ├── module-4-vla/     # VLA module content
│   ├── capstone/         # Capstone project content
│   ├── hardware/         # Hardware requirements content
│   └── cloud/            # Cloud deployment content
├── static/              # Static assets (images, etc.)
├── docusaurus.config.js # Docusaurus configuration
├── sidebars.js          # Navigation sidebar configuration
└── package.json         # Project dependencies and scripts
```

## Adding New Content

### Create a New Page
1. Create a new `.md` file in the appropriate module directory
2. Add frontmatter with the title:
```markdown
---
title: Page Title
---
```
3. Add your content in Markdown format

### Update Navigation
Update `sidebars.js` to include your new page in the navigation structure.

## Configuration

The main configuration is in `docusaurus.config.js`:
- Site metadata (title, description, etc.)
- Plugin configuration
- Theme customization
- Deployment settings

## Deployment

The site is configured for GitHub Pages deployment. When changes are pushed to the main branch, the site will be automatically built and deployed.