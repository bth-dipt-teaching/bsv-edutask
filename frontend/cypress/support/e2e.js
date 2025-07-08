// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'


Cypress.Commands.add('login', (email) => {
  cy.get('input[type=text]').type(email);
  cy.get('form').submit();
});

Cypress.Commands.add('loginProgrammatic', (user) => {
  cy.window().invoke('setUser', user);
});


Cypress.Commands.add('setupAndLogin', () => {
 
  let uid;
  let name;
  let email;

  
  return cy.fixture('user.json').then((userData) => {
    cy.request({
      method: 'POST',
      url: 'http://localhost:5000/users/create',
      form: true,
      body: userData,
    }).then((response) => {
        uid = response.body._id.$oid
        name = userData.firstName + ' ' + userData.lastName
        email = userData.email
      cy.visit('http://localhost:3000');
      cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

      cy.get('form')
      .submit()

      cy.wrap({ uid, name, email });
    });
  });
});


Cypress.Commands.add('createTodoItem', () => {
   const todoDescription = 'Food';
    const taskTitle = '#title';
    cy.get(taskTitle).type(todoDescription);
    const taskForm = '.submit-form.bordered';
    cy.get(taskForm).submit();
    cy.contains('.title-overlay', todoDescription).click();
});