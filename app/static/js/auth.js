// static/js/auth.js

const auth = {
    /**
     * Checks whether the user is authenticated by ensuring the access token exists in localStorage.
     * @returns {boolean} True if the user has a stored access token, false otherwise.
     */
    isAuthenticated: () => {
        const token = localStorage.getItem('access_token');
        return token !== null;
    },

    /**
     * Retrieves the access token from localStorage.
     * @returns {string|null} The access token if present, or null if not found.
     */
    getToken: () => {
        return localStorage.getItem('access_token');
    },

    /**
     * Saves the provided token to localStorage.
     * @param {string} token - The token to store.
     */
    saveToken: (token) => {
        localStorage.setItem('access_token', token);
    },

    /**
     * Removes the user token from localStorage, effectively logging the user out.
     */
    removeToken: () => {
        localStorage.removeItem('access_token');
    },

    /**
     * Performs a logout operation by removing the token and optionally redirecting.
     */
    logout: (redirectUrl = '/login') => {
        localStorage.removeItem('access_token');
        // Redirect the user to the login page
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
    },

    /**
     * Makes an authenticated API request. Will attach the stored token in the Authorization header.
     * @param {string} url - The API endpoint to call.
     * @param {Object} [options={}] - Additional fetch options (e.g., method, body).
     * @returns {Promise<Response>} The response from the API.
     */
    apiRequest: (url, options = {}) => {
        const token = auth.getToken();
        if (!token) {
            throw new Error('No access token found. Please authenticate first.');
        }

        const headers = {
            ...options.headers,
            Authorization: `Bearer ${token}`,
        };

        return fetch(url, {
            ...options,
            headers,
        });
    },
};

export default auth;