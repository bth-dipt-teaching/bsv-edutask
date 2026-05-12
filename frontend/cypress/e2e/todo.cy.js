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


const addToDo = (todoText) => {
    cy.get('.todo-list', { timeout: 2000 }).within(() => {
      cy.get('form.inline-form').within(() => {
        cy.get('input[type=text]').type(todoText); 
        cy.get('input[type=submit]').click();
      });
    });
  };

  it('R8UC1 add a to do TC1', () => {
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

   it('R8UC1 add a to do TC2', () => {
    cy.get('.todo-list').within(() => {
      cy.get('form.inline-form').within(() => {
        cy.get('input[type=text]').should('be.empty');
        cy.get('input[type=submit]').should('be.disabled'); 
      });
    });
  });


  it('R8UC2 toggle TC1', () => {
    const todoText = 'Buy groceries';

    addToDo(todoText);

    cy.contains('.todo-item', todoText, { timeout: 1000 }).should('exist').within(() => {
      cy.get('.checker', { timeout: 1000 }).click();
      cy.get('.checker').should('have.class', 'checked');

      cy.get('.checker', { timeout: 1000 }).click();
      cy.get('.checker').should('not.have.class', 'checked');
    });
  });


  it('R8UC3 delete', () => {
    const todoText = 'Buy groceries';

    addToDo(todoText);

    cy.contains('.todo-item', todoText, { timeout: 1000 }).should('exist')

    cy.contains('.todo-item' , todoText).find('.remover').click();

    cy.contains('.todo-item', todoText).should('not.exist');
  });


  after(() => {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    });
  });
});