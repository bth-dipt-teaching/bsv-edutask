describe('R8UC3 – Delete Todo Item', () => {
  let userId, userName, userEmail;
  const TASK_TITLE = 'Delete Test Task';
  const VIDEO_KEY = 'kcVRR1Qx4jA';
  const TODO_TEXT = 'Delete me 999';

  before(() => {
    cy.fixture('user.json').then(user => {
      const formBody = new URLSearchParams(user).toString();
      return cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formBody
      }).then(res => {
        if (res.status !== 200 && res.status !== 201) {
          throw new Error(`User creation failed: ${JSON.stringify(res.body)}`);
        }
        userId = res.body._id?.$oid || res.body._id;
        userName = `${user.firstName} ${user.lastName}`;
        userEmail = user.email;
      });
    });
  });

  after(() => {
    if (userId) {
      cy.request('DELETE', `http://localhost:5000/users/${userId}`);
    }
  });

  beforeEach(() => {
    cy.visit('http://localhost:3000');

    cy.contains('div', 'Email Address').find('input[type="text"]').type(userEmail);
    cy.get('form').submit();
    cy.contains('h1', `Your tasks, ${userName}`);

    cy.get('.inputwrapper #title').type(TASK_TITLE);
    cy.get('.inputwrapper #url').type(VIDEO_KEY);
    cy.get('.submit-form.bordered input[type="submit"]').click();
    cy.get(`img[src*="${VIDEO_KEY}"]`).last().click();

    // Add the uniquely named todo item before each test
    cy.get('.inline-form input[type="text"]').type(TODO_TEXT);
    cy.get('.inline-form input[type="submit"]').click();

    // Confirm todo item is added
    cy.contains('.todo-list li.todo-item', TODO_TEXT).should('exist');
  });

  it('deletes a todo item when clicking the × remover', () => {
    cy.intercept('DELETE', '**/todos/byid/*').as('deleteTodo');

    cy.contains('.todo-list li.todo-item', TODO_TEXT).as('targetTodo');

    cy.get('@targetTodo')
      .find('.remover')
      .should('be.visible')
      .click({ force: true });

    cy.wait('@deleteTodo').its('response.statusCode').should('eq', 200);

    cy.contains('.todo-list li.todo-item', TODO_TEXT).should('not.exist');
  });
});
