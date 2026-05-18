describe('Requirement 8: To-Do Item Management (R8UC1, R8UC2, R8UC3)', () => {
  
  beforeEach(() => {
    cy.fixture('user.json').as('userData');
    cy.fixture('task.json').as('testTask');
    cy.visit('/'); 

    cy.get('@userData').then((user) => {
      cy.get('input[name="email"]').type(user.email); 
    });
    cy.get('input[type="submit"]').click({ force: true });

    cy.get('body').then(($body) => {
      if ($body.text().includes('Top 7 Awesome Developer Tools')) {
        cy.contains('Top 7 Awesome Developer Tools').click();
      } else {
        cy.get('input[placeholder="Title of your Task"]').type('Top 7 Awesome Developer Tools');
        cy.get('input[placeholder*="Viewkey"]').type('dQw4w9WgXcQ'); 
        cy.get('input[type="submit"]').contains('Create new Task').click({force: true});
        cy.contains('Top 7 Awesome Developer Tools').click();
      }
    });
  });

  it('TC1 - should create a new to-do item (R8UC1)', function() {
    cy.get('input[placeholder*="Add"]').type(this.testTask.todos, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true }); 
    cy.contains(this.testTask.todos).should('be.visible');
  });

  it('TC2 - should toggle a to-do item status (R8UC2)', function() {
    cy.get('input[placeholder*="Add"]').type(this.testTask.todos, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true });

    cy.contains(this.testTask.todos)
      .parent()
      .find('.checker, .toggle, [type="checkbox"], svg')
      .first()
      .click({ force: true });
    
    cy.contains(this.testTask.todos).should('have.css', 'text-decoration').and('match', /line-through/);
  });

  it('TC3 - should delete a to-do item (R8UC3)', function() {
    const uniqueTodo = "Delete Me " + Date.now();
    cy.get('input[placeholder*="Add"]').type(uniqueTodo, { force: true });
    cy.get('input[type="submit"]').contains('Add').click({ force: true });

    cy.contains(uniqueTodo).should('exist');

    cy.contains(uniqueTodo)
      .parent()
      .find('.remover, .delete-icon, .remove-todo, .x-mark')
      .first()
      .click({ force: true });

    cy.reload();
    cy.get('body').then(($body) => {
      if (!$body.text().includes(uniqueTodo)) {
        return;
      } else {
        cy.contains('Top 7 Awesome Developer Tools').click();
      }
    });

    cy.contains(uniqueTodo).should('not.exist');
  });
});