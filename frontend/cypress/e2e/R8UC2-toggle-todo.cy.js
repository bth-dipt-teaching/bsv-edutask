describe('R8UC2 – Toggle Todo Status', function () {
  let userId, userName, userEmail;
  const TASK_TITLE = 'Toggle Test Task';
  const VIDEO_KEY = 'kcVRR1Qx4jA';

  before(function () {
    cy.fixture('user.json').then((user) => {
      const formBody = new URLSearchParams(user).toString();
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formBody
      }).then((res) => {
        if (res.status !== 200 && res.status !== 201) {
          throw new Error(`User creation failed: ${JSON.stringify(res.body)}`);
        }
        userId = res.body._id?.$oid || res.body._id;
        userName = `${user.firstName} ${user.lastName}`;
        userEmail = user.email;
      });
    });
  });

  after(function () {
    if (userId) {
      cy.request('DELETE', `http://localhost:5000/users/${userId}`);
    }
  });

  beforeEach(function () {
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input[type="text"]').type(userEmail);
    cy.get('form').submit();
    cy.contains('h1', `Your tasks, ${userName}`);

    cy.get('.inputwrapper #title').type(TASK_TITLE);
    cy.get('.inputwrapper #url').type(VIDEO_KEY);
    cy.get('.submit-form.bordered input[type="submit"]').click();

    cy.get(`img[src*="${VIDEO_KEY}"]`).last().click();
    cy.get('.todo-list li.todo-item').first().as('firstItem');
  });

  it('marks an active todo as done (adds "checked" class + strikethrough)', function () {
    cy.get('@firstItem')
      .find('.checker')
      .should('have.class', 'unchecked')
      .click()
      .should('have.class', 'checked');

    cy.get('@firstItem')
      .find('span')
      .eq(1)
      .should('have.css', 'text-decoration-line', 'line-through');
  });

  it('marks a done todo back to active (removes "checked" class + strikethrough)', function () {
    cy.get('@firstItem').find('.checker').then(($checker) => {
      if (!$checker.hasClass('checked')) {
        cy.wrap($checker).click();
      }
    });

    cy.get('@firstItem')
      .find('.checker.checked')
      .click()
      .should('have.class', 'unchecked');

    cy.get('@firstItem')
      .find('span')
      .eq(1)
      .should('have.css', 'text-decoration-line', 'none');
  });
});
