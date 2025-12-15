# Physical AI & Humanoid Robotics Book Constitution

## Project Overview
Unified Book on "Physical AI & Humanoid Robotics" built with Docusaurus using Spec-Kit Plus + Claude Code.

## Core Principles

### Technical Accuracy
- All content must be technically accurate for robotics, ROS 2, NVIDIA Isaac, Gazebo, and VLA systems
- Follow official ROS 2, Gazebo, NVIDIA Isaac, and OpenAI documentation for definitions
- All engineering explanations must reference real-world robotic principles (kinematics, SLAM, control)
- Code samples must be validated (ROS 2 Humble, rclpy, Isaac Sim Python API)

### Clarity & Accessibility
- Target intermediate-to-advanced AI/robotics learners
- Maintain clarity in complex technical explanations
- Provide high-quality diagrams, code examples, and system flows

### Architectural Consistency
- Ensure consistency across simulation → control → perception → VLA pipeline
- Maintain embodied AI correctness (physical laws, sensors, kinematics)
- Keep terminology consistent (e.g., "Digital Twin," "Physical AI," "VLA pipeline")
- All module content must reflect the provided course framework

### Quality Standards
- All robotics definitions must follow official documentation
- All engineering explanations must reference real-world robotic principles
- Terminology must remain consistent across all modules
- Diagrams should reflect real robotic architectures (URDF, SLAM graph, navigation stack)
- Code samples must be validated against target platforms

## Key Standards

### Technical Standards
- All robotics definitions must follow official ROS 2, Gazebo, NVIDIA Isaac, and OpenAI documentation
- All engineering explanations must reference real-world robotic principles (kinematics, SLAM, control)
- Terminology must remain consistent (e.g., "Digital Twin," "Physical AI," "VLA pipeline")
- All module content must reflect the provided course framework
- Code samples must be validated (ROS 2 Humble, rclpy, Isaac Sim Python API)
- Diagrams should reflect real robotic architectures (URDF, SLAM graph, navigation stack)

### Content Standards
- Book must stay aligned with course structure and weekly modules
- Must include at least 1 complete walkthrough per module (ROS 2 → Gazebo → Isaac → VLA)
- Include hardware requirements, cloud-vs-local architecture, and Jetson deployment section
- Provide step-by-step instructions for students to build the final "Autonomous Humanoid" project

## Constraints

### Technical Constraints
- Must compile as a **Docusaurus v3** documentation website
- Sidebar must reflect module progression (Module 1 → Module 4 → Capstone → Hardware Appendix)
- Book size: 120–200 pages total
- Code samples must be compatible with ROS 2 Humble, rclpy, and Isaac Sim Python API

### Content Constraints
- Tone: instructional, expert, technical—but accessible
- Content must align with the given course content and final capstone requirements
- Modules must follow progression: Simulation → Control → Perception → VLA
- Include proper hardware requirements and deployment considerations

## Success Criteria

### Technical Success
- Book builds successfully in Docusaurus and deploys cleanly to GitHub Pages
- All code examples compile and run as documented
- All explanations technically correct and consistent
- Cross-references and navigation work properly

### Educational Success
- Students can follow step-by-step to build the final "Autonomous Humanoid" project
- Contains accurate module breakdown, code, diagrams, workflows, and labs
- Fully aligned with the given course content and final capstone requirements
- Provides clear learning pathways from basic concepts to advanced implementations

### Maintenance Success
- Automatically usable by Claude Code for future updates, rewrites, and expansions
- Modular structure allows for easy content updates
- Clear separation of concerns between different modules and topics

## Project Structure
- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Quality Assurance
- All technical content must be verified against official documentation
- Code examples must be tested in target environments
- Diagrams must accurately represent system architectures
- Cross-module consistency must be maintained
- Regular validation against course objectives required

## Version Information
**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12
