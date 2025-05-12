PS C:\Users\coold\Desktop\rag_agent> python rag_agent.py --pdf design.pdf --model gemini-2.0-flash --save_db
C:\Users\coold\Desktop\rag_agent\rag_agent.py:14: LangChainDeprecationWarning: Importing FAISS from langchain.vectorstores is deprecated. Please replace deprecated imports:

>> from langchain.vectorstores import FAISS

with new imports of:

>> from langchain_community.vectorstores import FAISS
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.vectorstores import FAISS
Initializing Smart RAG Agent with design.pdf
Extracting text from design.pdf...
Extracted 3910 characters from PDF
Creating vector database...
Split document into 5 chunks
Vector database created successfully
Setting up QA and BDD generation chains...
Chains set up successfully
Smart RAG Agent setup complete!
Vector database saved to vectorstore.faiss

=== Smart RAG Agent Interactive Mode ===
Type 'exit' to quit
Start a query with 'bdd:' to generate BDD scenarios
====================================

Enter your query: bdd: for login
Generating BDD scenarios for: for login
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== BDD Scenarios ===
```gherkin
Feature: User Login

  Scenario: Successful Login
    Given I am on the login page
    When I enter a valid username and password
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And the response status code should be 200

  Scenario: Unsuccessful Login - Invalid Credentials
    Given I am on the login page
    When I enter an invalid username and password
    And I click the "Login" button
    Then I should see an error message
    And the response status code should be 401

  Scenario: Unsuccessful Login - Empty Username
    Given I am on the login page
    When I enter an empty username and a valid password
    And I click the "Login" button
    Then I should see an error message
    And the response status code should be 401

  Scenario: Unsuccessful Login - Empty Password
    Given I am on the login page
    When I enter a valid username and an empty password
    And I click the "Login" button
    Then I should see an error message
    And the response status code should be 401

  Scenario: Unsuccessful Login - Empty Username and Password
    Given I am on the login page
    When I enter an empty username and an empty password
    And I click the "Login" button
    Then I should see an error message
    And the response status code should be 401
```
===================

Enter your query: bdd: scenario of money transfer
Generating BDD scenarios for: scenario of money transfer
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== BDD Scenarios ===
```gherkin
Feature: Money Transfer

  Background:
    Given the user is logged in and on the Dashboard page

  Scenario: Successful money transfer
    Given the user's account balance is $100
    And the recipient "user2" exists
    When the user enters "user2" as the recipient
    And the user enters "50" as the amount to transfer
    And the user clicks the "Transfer" button
    Then the transfer should be successful
    And the user should see a success message
    And the user's account balance should be $50
    And the recipient "user2" should have received $50

  Scenario: Unsuccessful money transfer due to insufficient funds
    Given the user's account balance is $20
    And the recipient "user3" exists
    When the user enters "user3" as the recipient
    And the user enters "50" as the amount to transfer
    And the user clicks the "Transfer" button
    Then the transfer should fail
    And the user should see an error message "Insufficient funds"
    And the user's account balance should remain $20
    And the recipient "user3" should not have received any money

  Scenario: Unsuccessful money transfer due to invalid amount
    Given the user's account balance is $100
    When the user enters "user4" as the recipient
    And the user enters "-10" as the amount to transfer
    And the user clicks the "Transfer" button
    Then the transfer should fail
    And the user should see an error message "Invalid amount"
    And the user's account balance should remain $100

  Scenario: Unsuccessful money transfer due to non-existent recipient
    Given the user's account balance is $100
    When the user enters "nonexistent_user" as the recipient
    And the user enters "20" as the amount to transfer
    And the user clicks the "Transfer" button
    Then the transfer should fail
    And the user should see an error message "Recipient not found"
    And the user's account balance should remain $100
```
===================

Enter your query: bdd: for logout
Generating BDD scenarios for: for logout
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== BDD Scenarios ===
```gherkin
Feature: Logout

  Background: User is logged in
    Given the user is on the dashboard page
    And the user is authenticated

  Scenario: Successful logout redirects to the login page
    When the user clicks the "Logout" button
    Then the user should be redirected to the login page

  Scenario: Logout clears the user session
    Given the user is logged in
    When the user clicks the "Logout" button
    Then the user should not be able to access the dashboard without logging in

  Scenario: Logout button is present on the dashboard
    Given the user is on the dashboard page
    Then the "Logout" button should be visible
```
===================

Enter your query: bdd: for invalid money transfer
Generating BDD scenarios for: for invalid money transfer
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== BDD Scenarios ===
```gherkin
Feature: Money Transfer - Invalid Transfer Scenarios

  Background:
    Given the user is logged in and on the Dashboard page

  Scenario: Attempt to transfer a negative amount
    Given the user's account balance is 100
    When the user enters "-10" in the "Amount" field
    And the user selects "recipient_user" in the "To User" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Invalid amount"
    And the user's account balance should remain 100

  Scenario: Attempt to transfer zero amount
    Given the user's account balance is 100
    When the user enters "0" in the "Amount" field
    And the user selects "recipient_user" in the "To User" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Invalid amount"
    And the user's account balance should remain 100

  Scenario: Attempt to transfer an amount exceeding the account balance
    Given the user's account balance is 50
    When the user enters "100" in the "Amount" field
    And the user selects "recipient_user" in the "To User" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Insufficient funds"
    And the user's account balance should remain 50

  Scenario: Attempt to transfer to a non-existent user
    Given the user's account balance is 100
    When the user enters "20" in the "Amount" field
    And the user selects "non_existent_user" in the "To User" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Invalid recipient"
    And the user's account balance should remain 100

  Scenario: Attempt to transfer with an empty amount field
    Given the user's account balance is 100
    When the user leaves the "Amount" field empty
    And the user selects "recipient_user" in the "To User" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Invalid amount"
    And the user's account balance should remain 100
```
===================

Enter your query: what problem does this system try to solve
Answering question: what problem does this system try to solve
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== Answer ===
The Banking Application is designed to allow users to manage their bank accounts securely. It provides functionalities for user authentication (login/signup) and core banking operations (e.g., viewing balances and transferring money).
==============

Enter your query: what are the different api routes
Answering question: what are the different api routes
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== Answer ===
The API routes are:
- POST /api/login
- POST /api/signup
- POST /api/transfer
==============

Enter your query: what all functions are available in dashboard
Answering question: what all functions are available in dashboard
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== Answer ===
The dashboard has the following functionalities:
*   Displays the user’s account balance.
*   Allows money transfers by selecting a recipient and entering an amount.
==============

Enter your query: bdd: for dashboard
Generating BDD scenarios for: for dashboard
C:\Users\coold\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\langchain_google_genai\chat_models.py:390: UserWarning: Convert_system_message_to_human will be deprecated!
  warnings.warn("Convert_system_message_to_human will be deprecated!")

=== BDD Scenarios ===
```gherkin
Feature: Dashboard - Money Transfer

  Background:
    Given the user is logged in and on the Dashboard page

  Scenario: Successful money transfer
    Given the user's account balance is $100
    And the recipient's username is "recipient_user"
    When the user enters "recipient_user" in the "To User" field
    And the user enters "50" in the "Amount" field
    And the user clicks the "Transfer" button
    Then the user should see a success message
    And the user's account balance should be $50
    And the recipient's account balance should be updated accordingly

  Scenario: Unsuccessful money transfer - Insufficient funds
    Given the user's account balance is $20
    And the recipient's username is "recipient_user"
    When the user enters "recipient_user" in the "To User" field
    And the user enters "50" in the "Amount" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Insufficient funds"
    And the user's account balance should remain $20

  Scenario: Unsuccessful money transfer - Invalid amount
    Given the user's account balance is $100
    And the recipient's username is "recipient_user"
    When the user enters "recipient_user" in the "To User" field
    And the user enters "-10" in the "Amount" field
    And the user clicks the "Transfer" button
    Then the user should see an error message "Invalid amount"
    And the user's account balance should remain $100

  Scenario: Display user's account balance
    Given the user is logged in
    When the Dashboard page is loaded
    Then the user should see their account balance displayed

  Scenario: Redirect to Dashboard after successful login
    Given the user is on the Login page
    When the user enters valid credentials
    And the user clicks the "Login" button
    Then the user should be redirected to the Dashboard page
```
===================