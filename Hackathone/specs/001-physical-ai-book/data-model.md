# Data Model: book-physical-ai

## Content Entities

### Book Module
- **Name**: Module identifier (e.g., "ROS 2", "Gazebo", "NVIDIA Isaac", "VLA")
- **Title**: Display title for the module
- **Description**: Brief overview of the module content
- **Pages**: List of pages/chapters in the module
- **Prerequisites**: Knowledge required before starting this module
- **Learning Objectives**: What students will learn from this module

### Content Page
- **ID**: Unique identifier for the page
- **Title**: Display title of the page
- **Content**: Markdown content of the page
- **Module**: Reference to the parent module
- **Navigation Order**: Order within the module
- **Related Pages**: Cross-references to other pages

### Capstone Project
- **Title**: Name of the capstone project
- **Description**: Overview of the project
- **Requirements**: What components need to be integrated
- **Steps**: Sequential steps to complete the project
- **Integration Points**: How different modules connect

### Hardware Requirements
- **Component**: Name of the hardware component
- **Specifications**: Technical specifications
- **Purpose**: How the component is used in the project
- **Alternatives**: Alternative components that can be used
- **Cost Range**: Approximate cost range

### Cloud Deployment Options
- **Provider**: Cloud provider name
- **Services**: Specific services offered
- **Cost**: Pricing model
- **Performance**: Performance characteristics
- **Use Cases**: When to use this option

## Relationships

- Book Module contains multiple Content Pages
- Content Pages can reference other Content Pages (cross-references)
- Capstone Project integrates multiple Book Modules
- Hardware Requirements support Book Modules and Capstone Project
- Cloud Deployment Options apply to the overall project

## Validation Rules

- Each Book Module must have a unique name
- Each Content Page must have a unique ID within its module
- Navigation Order must be sequential without gaps
- All cross-references must point to existing pages
- Hardware requirements must specify units for all measurements