# money-on-my-mind 

*   Name: Daler Rahimov
*   Pitt ID: dar158

## Installation

1. Create a virtual environment for Python.
2. From the root of the repository run `pip install -r requirements.txt`
3. Add the `FLASK_APP` variable to your path. (e.g. `export FLASK_APP=budget.py`).

## Running the App

Once installed, the application can be started with Run `flask run --host 0.0.0.0 -p 5000` (Runs the service on `http://localhost:5000`)


## High-level description:

You will write a very simple budget application for a single user. Your application should support several budget categories, and a set monthly limit for each category (e.g., $700 for rent, $200 for food, $100 for gas, etc.). The application should allow the user to enter purchases and present an up to date list of the userâ€™s remaining budgeted amount in each category (e.g., you have $0/$700 left for rent, you are $20 over your food budget of $200, and you have $44/$100 left for gas), and the amount spent on uncategorized purchases. You can represent all server-side data as Python data structures, you do not need to use SQLAlchemy.

## Specifications:

1.  You must build a RESTful API for accessing your budget category and purchase resources. Specifically, users should be able to perform HTTP GETs, POSTs, and DELETEs on â€œ/catsâ€� to get a list of budget categories, add a new category, and delete a category (respectively), and also perform HTTP GETs and POSTs to â€œ/purchasesâ€� to get a list of individual purchases by the user and to add a new purchase.
    *   All data must be transmitted using JSON.
2.  Since we assume for this project that your website manages the budget of only a single user, you do not need to implement any user management, login, or password authentication.
3.  When the root resource of your site is accessed (â€œ/â€�), your Flask application should send a basic page skeleton to the user along with a JavaScript application that will make AJAX requests to populate the page.
4.  Once the page is loaded by a userâ€™s browser, it should make AJAX requests for the list of categories and list of purchases made by the user using the RESTful API.
5.  Because you are only outputting budget category summaries to the main page, use console.log() to print the contents of every AJAX response you get to ensure ease of grading.
6.  Once populated, the page should display the status of each of the userâ€™s budget categories, and the total of uncategorized purchases.
    *   Using Array.map(), Array.reduce(), and/or Array.filter() could be helpful in writing succinct code to perform your budget analysis.
7.  The user should always have the ability to add a new purchase (specifying the amount spent, what it was spent on, the date that it was spent, and the category it should be counted towards) or category (specifying name and limit), and also always have the ability to delete any existing category.
8.  You do not need to regularly poll the server for updates. However, once user requests any changes (e.g., add a purchase, add a category, delete a category), your application should fetch updated information via the RESTful API, and recompute the status of each of the userâ€™s budget categories.
9.  Because we are not storing the data using SQLAlchemy, you do not need to persist data across server instances.
    *   If the server is killed (i.e., Ctrl+C issued), all category/purchase data can be forgotten.
10.  You must build your website using JavaScript, JSON, AJAX, Python 3.6 or greater, and Flask 0.12.

## Submission Guidelines:

*   **DO NOT SUBMIT** any IDE package files.
*   You must name the main flask file for your site â€œbudget.pyâ€�, and place it in the root directory of your repository.
*   You must be able to run your application by setting the FLASK_APP environment variable to your budget.py and running â€œflask runâ€�
*   You must fill out [README.md](../errata/readme.html).
*   Be sure to remember to push the latest copy of your code back to your GitHub repository before the the assignment is due. At the deadline, the repositories will automatically be copied for grading. Whatever is present in your GitHub repository at that time will be considered your submission for this assignment.

## Additional Notes/Hints:

*   While you are not going to be heavily graded on the style and design of your web site, it should be presented in a clear and readable manner.
*   Using the JavaScript Date() class, you can construct a date object, and use that to figure out the current month.
*   While you are not explicitly required to use Flask-restful, you are certainly allowed to use it to build a RESTful API. If you decide against using Flask-restful, be sure to take care in building a truly RESTful API.
*   The lack of persistent data may lead to unwieldly debugging. You may find it helpful to use cURL (https://curl.haxx.se/docs/manpage.html) to automate a series of test insteractions with the RESTful API.

## Grading Rubric:

*   Data is fetched correctly: 10%
*   Add category works correctly: 10%
*   Delete category works correctly: 10%
*   Add purchase works correctly: 10%
*   RESTful API properly implemented: 15%
*   Proper analysis of budget performed: 25%
*   All AJAX responses (to POST and GET requests) are clearly printed to the JS console: 10%
*   Clear and readable presentation: 5%
*   Submission/readme: 5%
