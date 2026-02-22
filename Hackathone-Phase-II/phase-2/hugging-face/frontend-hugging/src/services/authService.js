// Frontend authentication service for handling JWT tokens and session management

class AuthService {
  constructor() {
    this.tokenKey = 'authToken';
    this.refreshTokenKey = 'refreshToken';
  }

  /**
   * Store authentication tokens
   */
  setTokens(accessToken, refreshToken = null) {
    if (accessToken) {
      localStorage.setItem(this.tokenKey, accessToken);
    }
    if (refreshToken) {
      localStorage.setItem(this.refreshTokenKey, refreshToken);
    }
  }

  /**
   * Get access token
   */
  getAccessToken() {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Get refresh token
   */
  getRefreshToken() {
    return localStorage.getItem(this.refreshTokenKey);
  }

  /**
   * Remove all tokens (logout)
   */
  clearTokens() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshTokenKey);
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const token = this.getAccessToken();
    if (!token) {
      return false;
    }

    // Check if token is expired
    return !this.isTokenExpired(token);
  }

  /**
   * Check if token is expired
   */
  isTokenExpired(token) {
    try {
      const payload = this.parseJwt(token);
      if (!payload.exp) {
        return true; // If no expiration, consider it expired
      }

      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true; // If there's an error parsing, consider it expired
    }
  }

  /**
   * Parse JWT token to extract payload
   */
  parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
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
   * Refresh access token using refresh token
   */
  async refreshToken() {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        this.setTokens(data.accessToken, data.refreshToken);
        return data.accessToken;
      } else {
        // Refresh failed, clear tokens
        this.clearTokens();
        throw new Error('Token refresh failed');
      }
    } catch (error) {
      console.error('Error refreshing token:', error);
      this.clearTokens(); // Clear tokens if refresh fails
      throw error;
    }
  }

  /**
   * Login user and store tokens
   */
  async login(email, password) {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();

        // Store tokens
        this.setTokens(data.token, data.refreshToken);

        return {
          success: true,
          user: data.user,
          token: data.token,
        };
      } else {
        const errorData = await response.json();
        return {
          success: false,
          error: errorData.message || 'Login failed',
        };
      }
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        error: 'Network error occurred',
      };
    }
  }

  /**
   * Logout user and clear tokens
   */
  logout() {
    this.clearTokens();

    // Optionally notify backend to invalidate the token
    const token = this.getAccessToken();
    if (token) {
      fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }).catch(error => {
        console.error('Error during logout:', error);
      });
    }
  }

  /**
   * Get user info from token
   */
  getUserFromToken() {
    const token = this.getAccessToken();
    if (!token || this.isTokenExpired(token)) {
      return null;
    }

    const payload = this.parseJwt(token);
    if (!payload) {
      return null;
    }

    return {
      id: payload.sub || payload.userId,
      email: payload.email,
      // Add other user properties as needed
    };
  }
}

// Export singleton instance
const authService = new AuthService();
export default authService;