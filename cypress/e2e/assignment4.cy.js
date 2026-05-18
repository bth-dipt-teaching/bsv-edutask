describe('Requirement 8: To-Do Item Management (R8UC1, R8UC2, R8UC3)', () => {
  
beforeEach(() => {
    // Load both fixtures
    cy.fixture('user.json').as('userData');
    cy.fixture('task.json').as('testTask');
    
    cy.visit('/'); 

    // Use the alias 'userData' to get the email from your JSON file
    cy.get('@userData').then((user) => {
      cy.get('input[name="email"]').type(user.email); // Types "mon.doe@gmail.com"
    });

    // Type your password (standard for this lab is usually '1234' or 'password')
    cy.get('input[name="password"]').type('password'); 
    cy.get('button[type="submit"]').click();
  });
  
  it('should create a new to-do item (R8UC1)', function() {
    // Use the "todos" string from your fixture: "Study components"
    cy.get('.todo-input').type(this.testTask.todos);
    cy.get('.add-todo-btn').click();
    
    // Verify the item is visible in the list
    cy.contains(this.testTask.todos).should('be.visible');
  });

  it('should toggle a to-do item status (R8UC2)', function() {
    // Ensure the item exists, then click the toggle/checkbox
    cy.contains(this.testTask.todos).parent().find('input[type="checkbox"]').click();
    
    // Verify the visual state (usually a CSS class or property)
    cy.contains(this.testTask.todos).should('have.css', 'text-decoration', 'line-through');
  });

  it('should delete a to-do item (R8UC3)', function() {
    // Find the item and click the delete button
    cy.contains(this.testTask.todos).parent().find('.delete-icon').click();
    
    // Verify the item is removed from the DOM
    cy.contains(this.testTask.todos).should('not.exist');
  });
});