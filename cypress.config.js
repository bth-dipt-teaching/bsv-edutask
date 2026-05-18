const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    // Change 5000 to 3000 to match your React frontend
    baseUrl: 'http://localhost:3000',
    supportFile: false // Keeps it simple for this assignment
  },

  component: {
    devServer: {
      framework: "create-react-app",
      bundler: "webpack",
    },
  },
});