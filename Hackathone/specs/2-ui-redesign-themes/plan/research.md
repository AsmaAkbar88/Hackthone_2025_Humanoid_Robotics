# Research Document: UI/UX Redesign with Strict Theme Requirements

## Decision: Theme Color Schemes (Strict Requirements)
**Rationale**: Strict adherence to the specified color constraints while ensuring accessibility.
- **Light Theme**: Primary #550000 (maroon) with white background and high-contrast text
- **Dark Theme**: Black and white only for maximum contrast and readability
- **Both themes meet WCAG AA contrast ratios** ensuring accessibility compliance

**Alternatives considered**:
- Additional colors for accents (rejected - violates strict color constraints)
- Different maroon shades (rejected - #550000 specifically required)
- Color variations for different elements (rejected - strict black/white constraint for dark theme)

## Decision: Front Page Layout Approach
**Rationale**: Implement a clear, structured layout that showcases the book content with improved visual hierarchy.
- **Hero Section**: Centered title with maroon accent and clear call-to-action
- **Navigation Grid**: Card-based layout for module navigation with consistent spacing
- **Content Hierarchy**: Clear visual separation between sections with proper typography
- **Responsive Design**: Mobile-first approach with adaptive layouts

**Alternatives considered**:
- Complex hero sections (rejected - simplicity preferred for academic use)
- Horizontal navigation (rejected - grid layout better for module organization)
- Minimalist approach (rejected - need clear visual hierarchy)

## Decision: Chapter Differentiation Strategy
**Rationale**: Each chapter should have a distinct visual structure while maintaining theme consistency.
- **Chapter 1 (ROS 2)**: Card-based layout with vertical sections
- **Chapter 2 (Gazebo/Unity)**: Full-width sections with horizontal dividers
- **Chapter 3 (NVIDIA Isaac)**: Sidebar navigation with content panels
- **Chapter 4 (VLA)**: Grid-based layout with feature cards

**Alternatives considered**:
- Same layout for all chapters (rejected - need visual distinction)
- More radical differences (rejected - maintain consistency within theme)
- Advanced interactive elements (rejected - keep simple for readability)

## Decision: Typography System
**Rationale**: Implement a clean, professional typography hierarchy using system fonts.
- **Primary Font**: Inter or system font stack (Inter, Roboto, Helvetica, Arial, sans-serif) for optimal readability
- **Monospace Font**: SFMono-Regular, Consolas, or Monaco for code elements
- **Font Sizes**: Consistent scale using rem units for accessibility scaling

**Alternatives considered**:
- Custom Google Fonts (rejected - increased load time, stick with system fonts)
- Original Docusaurus font stack (updated to more modern system fonts)

## Decision: Component Styling (Buttons, Icons, Navigation)
**Rationale**: Modern, accessible components that follow the strict theme requirements.
- **Buttons**: Rounded corners (8px), proper spacing, and hover states with maroon backgrounds for light theme
- **Navigation**: Clear visual hierarchy with maroon accents for light theme, white/black for dark theme
- **Icons**: Minimal, clean design that matches active theme
- **Spacing**: Consistent 8px base unit system for all components

**Alternatives considered**:
- Complex button styles (rejected - keep simple for academic use)
- Decorative icons (rejected - minimal design required)
- Non-standard spacing (rejected - consistent spacing system required)

## Decision: Layout and Spacing System
**Rationale**: Implemented consistent spacing using a modular scale approach for professional, harmonious layouts.
- **Grid System**: Flexible, responsive grid using CSS Grid and Flexbox
- **Spacing Scale**: Consistent 8px base unit (8px, 16px, 24px, 32px, 48px, 64px)
- **Component Padding**: Consistent internal spacing for cards, buttons, and content areas

**Alternatives considered**:
- Original spacing system (updated for better visual hierarchy)
- Complex spacing scales (chose simpler, more maintainable approach)

## Decision: Theme Switching Implementation
**Rationale**: Leveraged Docusaurus' built-in color mode API for seamless theme switching with localStorage persistence.
- **Implementation**: Uses `colorMode.respectPrefersColorScheme: true` for system preference respect
- **UI**: Theme toggle button in header with clear visual indicator
- **Persistence**: Remembers user preference across sessions

**Alternatives considered**:
- Custom theme switching (unnecessary - Docusaurus provides robust solution)
- Auto-switching based on time (rejected - user preference should prevail)

## Decision: Accessibility Compliance
**Rationale**: Ensured all design decisions maintain WCAG AA compliance despite strict color constraints.
- **Contrast Ratios**: All text/background combinations meet or exceed WCAG AA standards
- **Focus States**: Clear visual indicators for keyboard navigation
- **Semantic Structure**: Proper HTML elements for screen readers
- **Color Independence**: Functionality not dependent on color alone

**Alternatives considered**:
- Lower contrast for aesthetic reasons (rejected - accessibility takes precedence)
- Color-dependent functionality (rejected - maintain accessibility standards)