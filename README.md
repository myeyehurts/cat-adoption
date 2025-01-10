# catadoption

## Prerequisites 

* It is expected you already have Git, Python, and PyCharm installed (based on information given in class). Any other dependencies will be installed during the process.

## Setting up the application

1) Use the terminal to navigate to the folder you want your project stored in (e.g. `cd ~Documents/Code`).
2) Clone this repository by running `git clone https://github.com/Carleton-BIT/project-myeyehurts.git`.
3) Open the repository in PyCharm. You can do this using File->Open and selecting the folder called `project-myeyehurts`.
4) Make sure you have a Python interpreter set up. Go to `File->Settings->Project:project-myeyehurts->Python Interpreter`. If the dropdown menu at the top says "No Interpreter", select one from the list. If there are none listed, make one by clicking `Add Interpreter->Local Interpreter` and select an available version of Python for it. Make sure you apply the changes.
5) If you have just set up an interpreter, restart PyCharm.
6) Open a terminal inside PyCharm and install dependencies by running `pip install -r requirements.txt`. There should not be any issues with pip not being recognized if the interpreter is configured properly.
7) Create a file called `.env` in the top level directory (should be in the same folder as manage.py).
8) Generate a secret key by running `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in the terminal. Copy the output.
9) Edit `.env` (created in part 5) and add a line that says `SECRET_KEY="your-secret-key-here"`. Paste the output from part 6 into 'your-secret-key-here'.
10) On the PyCharm terminal, run `python manage.py migrate`.
11) Run the server by clicking the play button or running `python manage.py runserver` on the terminal.
12) Navigate to 127.0.0.1:8000 using the link provided in the terminal or by pasting the address into your browser. You should be viewing the homepage with the header `Cat Adoption`.
13) Create a superuser by running `python manage.py createsuperuser`. Follow the terminal prompts to create a user account. Note that the superuser won't have a profile picture due to the nature of how it is created in the terminal, but you can add one in the admin view if you wish.
14) Use the account you have set up to log into the Django admin view at `http://localhost:8000/admin`. 
15) Add some cats into the database by selecting `Cats->Add` under `CATADOPTION`. Follow the prompts to provide the required data and make sure to save the created cats.
* Now that the application is set up, I recommend you log out of the superuser to get the proper user experience.

## How to use the application

* You can browse the cats available by navigating to `http://localhost:8000/cats` or clicking the `Cats` button in the navbar. There are also filters to narrow down the selection of cats presented to you by categories such as breed, age, etc.
* Any further actions will require you to set up an account. This can be done by navigating to `http://localhost:8000/register` or clicking the `Register` button in the nav bar.
* Upon creating an account you will automatically be redirected to fill out an adoption profile which keeps relevant information on file for whenever you apply to adopt a cat. If you somehow skip the profile creation, attempting to access any service requiring it will take you back to fill one out.
* Upon filling out an adoption profile you can view or edit it on the View/Edit Profile page, accessed by clicking the button in the nav bar or navigating to `http://localhost:8000/view_or_edit_profile`.
* Once you have an adoption profile filled out you can request to adopt cats. This is done by clicking the `Adopt` button on the `Cats` page corresponding to the particular cat you want to adopt. 
* Your adoption requests can be viewed by clicking the `View Requests` button in the nav bar or navigating to `http://localhost:8000/adoption_requests`.
* You have the ability to cancel requests as long as they have a status of `pending`. If they are marked `decision made` (which would theoretically be done by an admin) this option is not made available.
* Once you are finished interacting with the website you can log out using the `Log out` button in the nav bar.

