/**
 * Utility functions for handling JWT tokens
 */

/**
 * Parse JWT token to extract payload
 * @param {string} token - JWT token to parse
 * @returns {Object|null} - Parsed payload or null if invalid
 */
export function parseJwt(token) {
  try {
    if (!token) {
      return null;
    }

    // Remove 'Bearer ' prefix if present
    const cleanToken = token.startsWith('Bearer ') ? token.substring(7) : token;

    const base64Url = cleanToken.split('.')[1];
    if (!base64Url) {
      return null;
    }

    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error parsing JWT:', error);
    return null;
  }
}

/**
 * Check if a token is expired
 * @param {string} token - JWT token to check
 * @returns {boolean} - True if expired, false otherwise
 */
export function isTokenExpired(token) {
  if (!token) {
    return true;
  }

  const payload = parseJwt(token);
  if (!payload || !payload.exp) {
    return true; // If no expiration, consider it expired
  }

  const currentTime = Math.floor(Date.now() / 1000);
  return payload.exp < currentTime;
}

/**
 * Check if a token will expire soon (within 5 minutes)
 * @param {string} token - JWT token to check
 * @returns {boolean} - True if expiring soon, false otherwise
 */
export function isTokenExpiringSoon(token) {
  if (!token) {
    return true;
  }

  const payload = parseJwt(token);
  if (!payload || !payload.exp) {
    return true; // If no expiration, consider it expiring soon
  }

  const currentTime = Math.floor(Date.now() / 1000);
  const fiveMinutesInSeconds = 5 * 60; // 5 minutes in seconds

  return payload.exp < (currentTime + fiveMinutesInSeconds);
}

/**
 * Get token expiration time
 * @param {string} token - JWT token to check
 * @returns {Date|null} - Expiration date or null if invalid
 */
export function getTokenExpiration(token) {
  if (!token) {
    return null;
  }

  const payload = parseJwt(token);
  if (!payload || !payload.exp) {
    return null;
  }

  // Convert Unix timestamp to Date
  return new Date(payload.exp * 1000);
}

/**
 * Get time until token expiration
 * @param {string} token - JWT token to check
 * @returns {number} - Milliseconds until expiration, negative if expired
 */
export function getTimeUntilExpiration(token) {
  if (!token) {
    return 0;
  }

  const expiration = getTokenExpiration(token);
  if (!expiration) {
    return 0;
  }

  return expiration.getTime() - Date.now();
}

/**
 * Get user ID from token
 * @param {string} token - JWT token to check
 * @returns {string|null} - User ID or null if not found
 */
export function getUserIdFromToken(token) {
  if (!token) {
    return null;
  }

  const payload = parseJwt(token);
  if (!payload) {
    return null;
  }

  return payload.sub || payload.userId || null;
}

/**
 * Get user email from token
 * @param {string} token - JWT token to check
 * @returns {string|null} - User email or null if not found
 */
export function getUserEmailFromToken(token) {
  if (!token) {
    return null;
  }

  const payload = parseJwt(token);
  if (!payload) {
    return null;
  }

  return payload.email || null;
}