export const API_URL = import.meta.env?.BACKEND_URL || 'http://localhost:8000';
export const API_TIMEOUT = 30000; // 30 seconds (was 10s)
export const MIN_QUERY_LENGTH = 5;
export const MAX_QUERY_LENGTH = 2000;
export const MIN_HIGHLIGHT_LENGTH = 5;
export const MAX_HIGHLIGHT_LENGTH = 500;
export const MAX_MESSAGES_PER_SESSION = 50;

export const BREAKPOINTS = {
  mobile: 768,
  tablet: 1199,
  desktop: 1200,
};

export const isMobile = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth < BREAKPOINTS.mobile;
};

export const isTablet = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth >= BREAKPOINTS.mobile && window.innerWidth < BREAKPOINTS.desktop;
};

export const isDesktop = () => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth >= BREAKPOINTS.desktop;
};
