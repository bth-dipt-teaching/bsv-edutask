describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  beforeEach(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body:user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        }).then(() => {
              cy.fixture('task.json').then((task) => {
              cy.request({
                method: 'POST',
                url: 'http://localhost:5000/tasks/create',
                form: true,
                body: {
                  ...task,
                  userid: uid
                }
      });
    });
      })
        
        .then(() => {
          cy.visit('http://localhost:3000');
          cy.get('[name="email"]').type(email);
          cy.get('[type="submit"]').click();
          cy.contains('Learn React').click();
        });
      });
    });

    afterEach(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    });
  });

    it('should not create a new todo when description is empty', () => {
      cy.get('.inline-form > [type="text"]').clear();

      cy.get('.inline-form > [type="submit"]')
        .should('be.disabled')
    })

    it('should create a new todo item', () => {
      cy.get('.inline-form > [type="text"]').type('Test Todo');
      cy.get('.inline-form > [type="submit"]').click();

     cy.get('.todo-list').children('.todo-item').last().should('contain.text', 'Test Todo');

    })

    it('should set active todo item to done and strike it through', () => {
      cy.contains('.todo-item', 'Study components').as('todotestitem');

      cy.get('@todotestitem').find('span.checker').click()

      cy.get('@todotestitem').find('span.checker').should('have.class', 'checked')

      cy.get('@todotestitem').find('span.editable').should('have.css', 'text-decoration-line', 'line-through')
    })

    it('should set done todo item back to active', () => {
      cy.contains('.todo-item', 'Study components').as('todotestitem');

      cy.get('@todotestitem').find('span.checker').click()

      cy.get('@todotestitem').find('span.checker').should('have.class', 'checked')

      cy.get('@todotestitem').find('span.checker').click()

      cy.get('@todotestitem').find('span.checker').should('have.class', 'unchecked')

      cy.get('.todo-list .todo-item .editable').should('not.have.css', 'text-decoration-line', 'line-through')
    })


    it('deletes a todo item when pressing x button', () => {
      cy.contains('.todo-item', 'Study components').as('todoDeletetestitem');

      cy.get('@todoDeletetestitem').find('span.remover').click({ force: true });

      cy.contains('.todo-item', 'Study components').should('not.exist');
    })



  });
