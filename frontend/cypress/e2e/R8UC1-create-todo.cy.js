describe("R8UC1 – Create Todo with valid description", () => {
  let userId, userName, userEmail;

  before(() => {
    cy.fixture("user.json").then((user) => {
      // Convert JSON to form-urlencoded format
      const formBody = new URLSearchParams(user).toString();

      cy.request({
        method: "POST",
        url: "http://localhost:5000/users/create",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formBody,
        failOnStatusCode: false
      }).then((res) => {
        console.log("User create response:", res.body); // DEBUG

        if (res.status !== 200 && res.status !== 201) {
          throw new Error(`User creation failed: ${JSON.stringify(res.body)}`);
        }

        // Handle MongoDB _id format
        userId = res.body._id?.$oid || res.body._id;
        userName = `${user.firstName} ${user.lastName}`;
        userEmail = user.email;
      });
    });
  });

  after(() => {
    if (userId) {
      cy.request("DELETE", `http://localhost:5000/users/${userId}`);
    }
  });

  it("creates a task and adds a todo item", () => {
    cy.visit("http://localhost:3000");

    cy.contains("div", "Email Address").find("input[type=text]").type(userEmail);
    cy.get("form").submit();

    cy.contains("h1", `Your tasks, ${userName}`);

    cy.get(".inputwrapper #title").type("Test Task");
    cy.get(".inputwrapper #url").type("kcVRR1Qx4jA");
    cy.get("form").submit();

    cy.get("img[src*='kcVRR1Qx4jA']").click();

    cy.get(".inline-form input[type=text]").type("Buy milk");
    cy.get(".inline-form input[type=submit]").click();

    cy.get(".todo-list").contains("Buy milk").should("exist");
  });
});
