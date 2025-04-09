// static/js/utils.js

const utils = {
    /**
     * Format a date string or object into a readable format (e.g., "March 31, 2025").
     * @param {string|Date} date - The date to format.
     * @param {Object} [options={}] - Optional Intl.DateTimeFormat options.
     * @returns {string} A formatted date string.
     */
    formatDate: (date, options = { year: 'numeric', month: 'long', day: 'numeric' }) => {
        return new Date(date).toLocaleDateString(undefined, options);
    },

    /**
     * Handles errors by logging and optionally displaying an alert to the user.
     * @param {string} context - The context or module where the error occurred.
     * @param {Error} error - The error object to handle.
     */
    handleError: (context, error) => {
        console.error(`[${context}] Error:`, error.message);
        alert('An error occurred. Please try again.');
    },

    /**
     * Renders HTML content inside the provided DOM element.
     * @param {string} id - The ID of the target DOM element.
     * @param {string} content - The HTML content to render.
     */
    renderContent: (id, content) => {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = content;
        } else {
            console.error(`Element with ID "${id}" not found.`);
        }
    },

    /**
     * Validates an email address against a standard regular expression.
     * @param {string} email - The email address to validate.
     * @returns {boolean} True if the email is valid, false otherwise.
     */
    validateEmail: (email) => {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(String(email).toLowerCase());
    },
};

export default utils;