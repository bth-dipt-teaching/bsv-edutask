// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })


Cypress.Commands.add('loginWithFixture', (fixtureName = 'example') => {
  cy.fixture(fixtureName).then((fixture) => {
    cy.viewport(1280, 2000);
    cy.visit('http://localhost:3000/');
    cy.get('#email').type(fixture.email);
    cy.get('[type="submit"]').click();
    cy.wait(1000);
    cy.get('h1').should('contain.text', 'Your tasks, ' + fixture.firstName);
  });
});

Cypress.Commands.add('checkFirstTaskFixture', () => {
    // # Check if container-element has at least one element
    cy.get('.container-element').should('have.length.greaterThan', 0);
    cy.get('.container-element').first().within(() => {
      cy.get('a').click();
    });
  });

Cypress.Commands.add('createFirstTaskFixture', () => {
    cy.fixture('task.json')
      .then((task) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: {
            userid: Cypress.env("uid"),
            title: task.title,
            url: task.url,
            todos: "Todo 1",
            description: task.description,
          },
        }).then((response) => {
          console.log(response.body[0]._id.$oid)
          Cypress.env("taskid", response.body[0]._id.$oid)
          cy.log(`Task created with id ${response.body[0]._id.$oid}, title ${response.body[0].title} and description ${response.body[0].description}.`);
        })
      })
  });

Cypress.Commands.add('attachTodoFixture', (description, status) => {
    cy.fixture('task.json')
      .then((task) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/todos/create',
          form: true,
          body: {
            taskid: Cypress.env("taskid"),
            description: description,
            done: status,
          },
        })
      })
  });

Cypress.Commands.add('createUserFixture', () => {
    // create a fabricated user from a fixture
    cy.fixture('example.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          Cypress.env("uid", response.body._id.$oid)
          cy.log(`User created with id ${response.body._id.$oid}, name ${user.firstName + ' ' + user.lastName} and email ${user.email}.`);
        })
      })
  });
Cypress.Commands.add('deleteUserFixture', () => {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${Cypress.env("uid")}`
    }).then((response) => {
      cy.log(response.body)
    })

  });


