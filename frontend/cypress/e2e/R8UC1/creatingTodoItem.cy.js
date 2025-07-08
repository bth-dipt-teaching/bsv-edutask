describe('Todo Item Creation', () => {
  const todoDescription = 'Food';
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

    beforeEach(function () {
    // enter the main main page
      cy.visit('http://localhost:3000');
      cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

      cy.get('form')
      .submit()
  })


  it('the todo item should be deleted and removed from the list when the delete button is clicked', () => {
    cy.createTodoItem();
    const inputSelector = '.inline-form input[type="text"]';
    cy.get(inputSelector).type(todoDescription);
    const addButtonSelector = '.inline-form input[type="submit"]';
    cy.get(addButtonSelector).click();
    cy.contains('li.todo-item', todoDescription).should('be.visible');
    cy.contains('li.todo-item', todoDescription).find('.remover').click();
    cy.contains('li.todo-item', todoDescription).should('not.exist');
  });

  it('todo item should be crossed over when clicked if active', () => {
    cy.createTodoItem();
    const inputSelector = '.inline-form input[type="text"]';
    cy.get(inputSelector).type(todoDescription);
    const addButtonSelector = '.inline-form input[type="submit"]';
    cy.get(addButtonSelector).click();
    cy.contains('li.todo-item', todoDescription).should('be.visible');
    cy.contains('li.todo-item', todoDescription).find('.checker.unchecked').click();
    cy.contains('li.todo-item', todoDescription).find('.checker').should('have.class', 'checked');
  });

  it('done todo item should be uncrossed when checker is pressed', () => {
    cy.createTodoItem();
    const inputSelector = '.inline-form input[type="text"]';
    cy.get(inputSelector).type(todoDescription);
    const addButtonSelector = '.inline-form input[type="submit"]';
    cy.get(addButtonSelector).click();
    cy.contains('li.todo-item', todoDescription).should('be.visible');
    cy.contains('li.todo-item', todoDescription).find('.checker.checked').click();
    cy.contains('li.todo-item', todoDescription).find('.checker').should('have.class', 'unchecked');
  }); 


  it('should allow a user to create a new todo item', () => {
    cy.createTodoItem();
    const inputSelector = '.inline-form input[type="text"]';
    cy.get(inputSelector).type(todoDescription);
    const addButtonSelector = '.inline-form input[type="submit"]';
    cy.get(addButtonSelector).click();
    cy.contains('li.todo-item', todoDescription).should('be.visible');
  });
  
  it('button should be disabled when no text is entered', () => {
    cy.createTodoItem();
    const inputSelector = '.inline-form input[type="text"]';
    cy.get(inputSelector).clear();
    const addButtonSelector = '.inline-form input[type="submit"]';
    cy.get(addButtonSelector).click().should('be.disabled');
  });


after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})