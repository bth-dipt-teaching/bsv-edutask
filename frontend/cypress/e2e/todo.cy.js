describe('To-Do Integration Test', () => {
  let uid, email, name;

  before(() => {
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((res) => {
        uid = res.body._id.$oid;
        email = user.email;
        name = user.firstName + ' ' + user.lastName;
      });
    });
  });

  beforeEach(() => {
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input').type(email);
    cy.get('form').submit();
    
    cy.get('form.submit-form').within(() => {
      cy.get('#title').type('Test Task');
      cy.get('#url').type('dQw4w9WgXcQ');
      cy.get('input[type=submit]').click();
    });

    // timeout is simply because it takes long time for the task to load in
    cy.get('.container-element a', { timeout: 100 }).first().click();
  });

  it('add a to do', () => {
    const todoText = 'Buy groceries';

    cy.get('.todo-list', { timeout: 1000 }).within(() => {
      cy.get('form.inline-form').within(() => {

        cy.get('input[type=text]').should('be.empty');
        cy.get('input[type=submit]').should('be.disabled');


        cy.get('input[type=text]').type(todoText);
        cy.get('input[type=submit]').should('not.be.disabled').click();


      });
    });

    cy.contains('.todo-item', todoText).should('exist');
  });

  after(() => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    });
  });
});