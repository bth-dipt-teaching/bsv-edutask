

describe('R8UC1', () => {
  let videoName = 'https://www.youtube.com/watch?v=bjh7EYdFTo4';
  let taskName = 'RandomTaskName';

  before(function () {
    cy.createUserFixture();
    cy.createFirstTaskFixture();
  })


  beforeEach('loadfixture', () => {
    cy.loginWithFixture(); 
    cy.checkFirstTaskFixture();
  });

  it("Empty field and disable button", () => {
    cy.get('form.inline-form').within(() => {
      cy.get('[type="text"]').clear();
      cy.log("This test should generate an error because the button is not designed correctly now")
      cy.get('[type="submit"]').should('be.disabled');
    });
  })

  it("Write something and not disable button", () => {
    cy.get('form.inline-form').within(() => {
      cy.get('[type="text"]').type(taskName);
      cy.get('[type="submit"]').should('not.be.disabled');
    });
  })

  it("Todo can be added at the end of the todo list", () => {
    // cy.viewport(1280, 2000);
    cy.get('form.inline-form').within(() => {
      cy.get('[type="text"]').type(taskName);
      cy.get('[type="submit"]').click();
    });
    // # Check if the task is added to the list
    cy.get('li.todo-item').last().within(() => {
      cy.contains(taskName, { timeout: 2000 }).should('exist');
    });
  })

  after(function () {
    cy.deleteUserFixture();
  })
});

describe('R8UC2', () => {
  before(function () {
    cy.createUserFixture();
    cy.createFirstTaskFixture();
    // cy.attachTodoFixture("Todo 2", true);
  })

  beforeEach('loadfixture', () => {
    cy.loginWithFixture();
    cy.checkFirstTaskFixture();
  });

  it('Set todo task as active', () => {
    cy.contains('.todo-item', 'Todo 1', { matchCase: true }).within(() => {

      cy.get('.checker').then(($el) => {
        const classList = $el.attr('class');
        if (!classList.includes('unchecked')) { 
          cy.wrap($el).click();
        }
        cy.wrap($el).should('have.attr', 'class').and('contain', 'unchecked');
        cy.get('.editable').should('not.have.css', 'text-decoration-line', 'line-through');
      })
    })
  })
  
  it('Set todo task as done', () => {
    cy.contains('.todo-item', 'Todo 1', { matchCase: true }).within(() => {
      cy.get('.checker').then(($el) => {
        const classList = $el.attr('class');
        if (classList.includes('unchecked')) {
          cy.wrap($el).click();
        }
        cy.wrap($el).should('have.attr', 'class').and('contain', 'checked');
        cy.get('.editable').should('have.css', 'text-decoration-line', 'line-through');
      })
      })
  })

  after(function () {
    cy.deleteUserFixture();
  })
})

describe('R8UC3', () => {
  before(function () {
    cy.createUserFixture();
    cy.createFirstTaskFixture();
    cy.attachTodoFixture("Todo 2", true);
  })
  beforeEach('loadfixture', () => {
    cy.loginWithFixture(); 
    cy.checkFirstTaskFixture(); 
  });

  it('Remove todo task', () => {
    let todoName = "Todo 2";

    // # Remove the task
    cy.contains('.todo-item', todoName, { matchCase: true }).within(() => {
    cy.get('.remover').click()
  });
    // # Check if the task is removed from the list
    cy.contains('.todo-item', todoName).should('not.exist');
  })
  after(function () {
    cy.deleteUserFixture();
  })
})

