# Data Model: UI/UX Styling Upgrade

## Theme Configuration
- **Entity**: ThemeConfig
- **Fields**:
  - themeType: string (dark|light)
  - primaryColor: string (based on theme - black/white or pink/off-white)
  - secondaryColor: string (complementary colors based on theme)
  - textColor: string (black for both themes as per constraints)
  - backgroundColor: string (background color based on theme)
  - accentColors: array of strings (supporting colors within theme constraints)

## Button Styles
- **Entity**: ButtonStyle
- **Fields**:
  - buttonType: string (primary, secondary, danger, edit, task, delete)
  - baseStyles: object (common styles across all buttons)
  - hoverStyles: object (theme-specific hover states)
  - activeStyles: object (styles for active/pressed state)
  - transitionProperties: object (animation and transition settings)
  - themeSpecificOverrides: object (variations based on selected theme)

## Typography Settings
- **Entity**: TypographyConfig
- **Fields**:
  - fontFamily: string (selected modern font family)
  - fontSizeScale: object (sizes for h1-h6, body, caption, etc.)
  - fontWeightScale: object (weights for different text elements)
  - lineHeightScale: object (line height ratios for readability)
  - letterSpacing: object (spacing adjustments for clarity)

## Layout Spacing System
- **Entity**: SpacingConfig
- **Fields**:
  - baseUnit: number (foundation spacing unit)
  - scale: array of numbers (multiples of base unit)
  - componentSpacing: object (specific spacing for components)
  - responsiveBreakpoints: object (spacing adjustments for different screen sizes)