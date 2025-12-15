---
id: 001
title: Create Project Constitution
stage: constitution
date: 2025-12-12
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: AsmaAkbar88
command: /sp.constitution
labels: [constitution, physical-ai, humanoid-robotics, docusaurus]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/001-create-project-constitution.constitution.prompt.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Unified Book on "Physical AI & Humanoid Robotics" built with Docusaurus using Spec-Kit Plus + Claude Code.

Core principles:
- Technical accuracy for robotics, ROS 2, NVIDIA Isaac, Gazebo, and VLA systems
- Clarity for intermediate-to-advanced AI/robotics learners
- Architectural consistency across simulation → control → perception → VLA
- Embodied AI correctness (physical laws, sensors, kinematics)
- High-quality diagrams, code examples, and system flows
- Book must stay aligned with course structure and weekly modules

Key standards:
- All robotics definitions must follow official ROS 2, Gazebo, NVIDIA Isaac, and OpenAI documentation
- All engineering explanations must reference real-world robotic principles (kinematics, SLAM, control)
- Terminology must remain consistent (e.g., "Digital Twin," "Physical AI," "VLA pipeline")
- All module content must reflect the provided course framework
- Code samples must be validated (ROS 2 Humble, rclpy, Isaac Sim Python API)
- Diagrams should reflect real robotic architectures (URDF, SLAM graph, navigation stack)

Constraints:
- Must compile as a **Docusaurus v3** documentation website
- Sidebar must reflect module progression (Module 1 → Module 4 → Capstone → Hardware Appendix)
- Tone: instructional, expert, technical—but accessible
- Book size: 120–200 pages total
- Must include hardware requirements, cloud-vs-local architecture, and Jetson deployment section
- Include at least 1 complete walkthrough per module (ROS 2 → Gazebo → Isaac → VLA)

Success criteria:
- Book builds successfully in Docusaurus and deploys cleanly to GitHub Pages
- All explanations technically correct and consistent
- Students can follow step-by-step to build the final "Autonomous Humanoid" project
- Contains accurate module breakdown, code, diagrams, workflows, and labs
- Fully aligned with the given course content and final capstone requirements
- Automatically usable by Claude Code for future updates, rewrites, and expansions
```

## Response snapshot

Created a comprehensive constitution file for the Physical AI & Humanoid Robotics book project. The constitution includes:

- Core principles covering technical accuracy, clarity, architectural consistency, and quality standards
- Key standards for technical and content requirements
- Constraints for technical implementation and content delivery
- Success criteria for technical, educational, and maintenance goals
- Project structure guidelines
- Quality assurance measures

The constitution aligns with all specified requirements including ROS 2, NVIDIA Isaac, Gazebo, and VLA systems coverage, Docusaurus v3 compilation, and educational accessibility for intermediate-to-advanced learners.

## Outcome

- ✅ Impact: Created foundational project constitution with all specified principles and constraints
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific content
- 🔁 Next prompts: Plan creation, specification development, task breakdown
- 🧠 Reflection: Constitution successfully captures all project requirements and provides clear governance for future development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All requirements implemented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification development based on constitution