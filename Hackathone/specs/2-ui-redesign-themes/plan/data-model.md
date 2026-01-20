# Data Model: UI/UX Redesign with Strict Theme Requirements

## Theme Configuration Entity

**Entity Name**: Theme Configuration
**Description**: Represents the current visual theme applied to the application interface with strict color constraints

**Attributes**:
- **themeId**: String (unique identifier for the theme - "light" or "dark")
- **primaryColor**: HexColor (main brand color for the theme - #550000 for light, #FFFFFF for dark)
- **backgroundColor**: HexColor (background color for main content areas)
- **textColor**: HexColor (primary text color for content)
- **secondaryColor**: HexColor (accent color for interactive elements)
- **codeBackgroundColor**: HexColor (background for code blocks)
- **contrastRatio**: Float (WCAG contrast ratio between text and background)

**Validation Rules**:
- themeId must be one of ["light", "dark"]
- For light theme: primaryColor must be #550000 (maroon), backgroundColor must be white
- For dark theme: all colors must be black or white only
- All color values must be valid hex color codes (#RRGGBB)
- contrastRatio must be >= 4.5 for normal text, >= 3.0 for large text (WCAG AA compliance)

**State Transitions**:
- Initial state: themeId = user's system preference or last saved preference
- Transition 1: User selects light theme → themeId = "light"
- Transition 2: User selects dark theme → themeId = "dark"

## Visual Asset Entity

**Entity Name**: Visual Asset
**Description**: Represents visual elements such as images, icons, and graphics used in the application

**Attributes**:
- **assetId**: String (unique identifier for the asset)
- **assetType**: Enum ["icon", "image", "illustration", "logo"]
- **fileFormat**: Enum ["svg", "png", "jpg", "webp"]
- **dimensions**: Object {width: Integer, height: Integer} (in pixels)
- **altText**: String (accessibility text for screen readers)
- **purpose**: String (description of the asset's role in the UI)
- **themeCompatibility**: Array of Strings (themes the asset works with)

**Validation Rules**:
- assetId must be unique across all visual assets
- fileFormat must be one of the allowed formats
- dimensions.width and dimensions.height must be positive integers
- altText must be provided for all non-decorative assets
- file size must be optimized (under 100KB for images, under 10KB for SVGs)
- For dark theme: assets must work with black/white only constraint

## UI Component Entity

**Entity Name**: UI Component
**Description**: Represents reusable interface elements that make up the application's user interface

**Attributes**:
- **componentName**: String (unique name of the component)
- **styleType**: Enum ["button", "card", "navigation", "form-element", "content-block"]
- **spacingRules**: Object {padding: String, margin: String} (CSS spacing values)
- **typography**: Object {fontFamily: String, fontSize: String, fontWeight: String}
- **colorVariables**: Object (mapping of CSS custom properties to values)
- **responsiveBehavior**: Object (breakpoints and responsive adjustments)
- **accessibilityFeatures**: Array of Strings (ARIA labels, keyboard navigation, etc.)

**Validation Rules**:
- componentName must be unique across all components
- All spacing values must follow the established spacing scale (multiples of 8px)
- typography.fontSize must use rem or em units for accessibility
- colorVariables must map to theme-compatible CSS custom properties
- accessibilityFeatures must include keyboard navigation support
- For light theme: only maroon (#550000) and white colors allowed
- For dark theme: only black and white colors allowed

## User Preference Entity

**Entity Name**: User Preference
**Description**: Stores user-specific preferences for the application interface

**Attributes**:
- **userId**: String (anonymous user ID or null for unauthenticated users)
- **selectedTheme**: String ("light" or "dark")
- **fontSizePreference**: String ("normal", "large", "larger") for accessibility
- **lastUpdated**: DateTime (timestamp of last preference change)
- **savedLayout**: String (identifier for any customized layout preferences)

**Validation Rules**:
- selectedTheme must be one of ["light", "dark"]
- fontSizePreference must be one of ["normal", "large", "larger"]
- lastUpdated must be a valid ISO 8601 datetime string
- userId can be null for anonymous users but must be unique when present

## Style Configuration Entity

**Entity Name**: Style Configuration
**Description**: Global styling parameters that define the visual design system with strict color constraints

**Attributes**:
- **spacingScale**: Array of Integers (pixel values for consistent spacing)
- **fontStack**: Array of Strings (ordered font family preferences)
- **borderRadiusValues**: Array of Strings (border-radius values for consistent shapes)
- **shadowDefinitions**: Array of Strings (box-shadow values for depth)
- **transitionSettings**: Object (duration and easing for UI transitions)
- **breakpointDefinitions**: Object (media query breakpoints for responsiveness)
- **themeColors**: Object (strict color definitions per theme)

**Validation Rules**:
- spacingScale values must be multiples of 4px for consistency
- fontStack must include at least one system font as fallback
- borderRadiusValues must be valid CSS border-radius values
- transitionSettings.duration must be in milliseconds (positive integer)
- themeColors must comply with strict color constraints:
  - Light theme: only #550000 (maroon) and white allowed
  - Dark theme: only black and white allowed

## Chapter Layout Entity

**Entity Name**: Chapter Layout
**Description**: Defines the unique visual structure for each of the 4 book chapters

**Attributes**:
- **chapterId**: String (identifier for the chapter - "module-1-ros2", "module-2-gazebo", etc.)
- **layoutType**: Enum ["card-based", "full-width", "sidebar-nav", "grid-based"]
- **spacingPattern**: Object (specific spacing rules for this chapter)
- **typographyPattern**: Object (specific typography rules for this chapter)
- **colorScheme**: Object (theme-specific color applications)
- **componentVariations**: Array of Strings (special component behaviors for this chapter)

**Validation Rules**:
- chapterId must be unique and correspond to actual chapter
- layoutType must be one of the predefined types
- All color applications must comply with strict theme constraints
- Each chapter must have a visually distinct layout from others
- All layouts must maintain accessibility standards