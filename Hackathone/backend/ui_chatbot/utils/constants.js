/**
 * Configuration constants for chatbot UI
 */

// API configuration
export const API_URL = process.env.BACKEND_URL || 'http://localhost:8000';
export const API_TIMEOUT = 10000; // 10 seconds

// Validation limits
export const MIN_QUERY_LENGTH = 5;
export const MAX_QUERY_LENGTH = 2000;
export const MIN_HIGHLIGHT_LENGTH = 5;
export const MAX_HIGHLIGHT_LENGTH = 500;
export const MAX_MESSAGES_PER_SESSION = 50;

// Device detection breakpoints
export const BREAKPOINTS = {
  mobile: 768,    // < 768px
  tablet: 1199,   // 768px - 1199px
  desktop: 1200,  // >= 1200px
};

/**
 * Detect if current device is mobile
 * @returns {boolean} True if mobile viewport
 */
export const isMobile = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth < BREAKPOINTS.mobile;
};

/**
 * Detect if current device is tablet
 * @returns {boolean} True if tablet viewport
 */
export const isTablet = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth >= BREAKPOINTS.mobile &&
         window.innerWidth < BREAKPOINTS.desktop;
};

/**
 * Detect if current device is desktop
 * @returns {boolean} True if desktop viewport
 */
export const isDesktop = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth >= BREAKPOINTS.desktop;
};

/**
 * Get current viewport type
 * @returns {string} 'mobile' | 'tablet' | 'desktop'
 */
export const getViewport = () => {
  if (isMobile()) return 'mobile';
  if (isTablet()) return 'tablet';
  return 'desktop';
};
