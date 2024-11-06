BMI calculator is a GUI app that enables one to calculate their bmi.

features include:
An intuitive and friendly user interface.
Allows for user input where users enter their weight and height.
A database that holds the users data.

Installation Dependencies:
python3.
customtkinter- Can be installed by running the cmd:"pip install customtkinter==0.3".
Psycopg2:It establishes a connection to the db.- Can be installed by running the comand:"pip install psycopg2".
dotenv-cmd:"pip install python-dotenv".


Steps for installation and running the app:
1: Clone the repo.
2: cd to the project dir and navigate to the bmi_calculator folder.
3: Install the above dependencies.
4: Open terminal and login to psql cmd line usin the cmd:"psql -U postgres"
5: create a new user, a new db and grant all the priviledges to the user.
6: create a ".env" file and create env variables, the ones in db.py, corresponding to the user, db and password.
7: run the file "bmi_calc.py" using the cmd:"python3 bmi_calc.py"

Contributions are welcome.Here's how you can contribute:
1:Create a new feature branch (git checkout -b feature-branch-name).
2:Commit your changes (git commit -m 'Add some feature').
3:Push to the branch (git push origin feature-branch-name).
4:Create a Pull Request.

License This project is licensed under the MIT License.

Contact:
Created by Adnan Gard Obuya-gardobuyaadnan@gmail.com.
Feel free to reach out for any questions or feedback