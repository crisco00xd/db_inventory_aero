# db_inventory_aero
 
This project was created using flask and is connected to a postgresql database.
 
## Development server
Prior to running the project locally, you will need to install the project dependencies using:
pip install -r requirements.txt 
It is recommended to run the project utilizing a virtual environment (like virtualenv or conda)
 
## Instructions for virtual env using anaconda
1. Install Anaconda and give it access to your PATH
2. Open a new terminal in the project directory
3. conda create [Environment name]
4. conda activate [Environment name]
Always activate your environment when you will
run the project and make sure you install the dependencies
In your virtual environment.

Once you have isntalled dependencies, you can start up the backend by running the App.py file. 
REMEMBER THAT WHEN WORKING ON THE FILES WHILE RUNNING THE APP.PY, CHANGES YOU MAKE WON'T BE REFLECTED 
EVEN IF YOU SAVE UNTIL YOU RERUN THE APP.PY FILE.

#### Local Database Prerequisites:
 
Install DBeaver and psql.
 
#### Connecting to the remote database:

Open DBbeaver and create a new postgres server connection using the Heroku credentials. 
 
#### Heroku credentials:
 
##### Host
ec2-34-236-215-156.compute-1.amazonaws.com
##### Database
d206k08qottimm
##### User
efalozdnlswiuk
##### Port
5432
##### Password
a81aba78488b90d9f6d846d45e04db658cd78219286f0a72a445e7cd1ff37b84
 
##### Once connected, you can view the data tables under:
 
###### D206k08qottimm > d206k08qottimm > Schemas > public > Tables
Right click on a data table and select view data, you should see the data currently on the main heroku server for whatever tab you’re on.
	
#### Connecting to a local database:
##### Create a new local PostgreSQL database using DBeaver or PGAdmin 4
##### Change the DEV_DB variable in 
###### api > util > config.py 
##### to match the username and password you created when you installed psql on your system.
##### Run app.py under DB_INVENTORY_AERO
##### Open DBeaver and create a new postgres server connection using the credentials from the DEV_DB link:
###### DEV_DB = 'postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE
#EXAMPLE LINK, USE A DIFFERENT USER/PASS. 'DATABASE' will have to be changed to whatever you called your localDB. USERNAME will be your postgres master user (normally postgres) and PASSWORD will be your postgres master password (normally set up when you use PG Admin 4 or Postgres for the first time)
##### Host
localhost
##### Database
rumair_inventory_db
##### User
postgres
##### Port
5432
##### Password
Mypass
##### Once connected, export the data from your first connection to the local database by shift clicking on the tables in the heroku database > clicking export data > exporting as a database table > select public from your local database as the export location and auto assign the data mapping > leave settings tab as default > confirm and start transfer
You should now have access to all the data from the heroku database on your local system, and will be able to run SQL queries on the database. 
 
 
## Adding features
 
Always work on separate branches for features.
Structure commit messages with:
   -[Feat] "thing you added"
   -[Fix] "Thing you fixed"
   -[Removed] "Thing you removed"
   - etc
Add descriptions to large commits. 
Create a Pull Request when your feature is complete and bugfree in order to merge to master.
 
 
## Branches & Special Files
 
Branch name structure:
All Lower case, separated by hyphens.
example: this-is-my-test-branch
 
 
For every assigned task have 1 branch. Don't lump in unrelated changes into the same branch. The 1 issue- 1 branch workflow makes merge requests a lot faster and convenient for revisions.
 
Don't stage/commit changes to pipfile-lock.json, pipfile.txt, requirements.txt, or config.py. These are files that shouldn't be changed unless the project as a whole is undergoing updating of dependencies. 
 
 
## Code Structure

Flask is a Python Micro-framework which we utilize as the backend. The code for any backend route is roughly broken down into:
[dao->example.py] -> the Dao folder contains the functions which actually run the SQL queries whilst connecting to the database. Flask comes with basic functions to q			   query SQL like .query.all(), but if you'd like to query raw SQL, just use the text function from SQLAlchemy 
			(ex: sql = text('SELECT * FROM  YourTable)' ), and then run db.engine.execute(sql). 
			
[handler->example.py]-> the Handler folder contaings the functions that unpack the results of your SQL Queries. SQL Queries are stored as iterable objects where each row of sql can be turned into a dictionary (which is a lot like a json object which makes it perfect to send back to the frontend). So to unpack a query of a series of items, you would write something like 'for item in items:' and in order to prepare each item you would pass it through either Utilities.to_dict(item) (if you used a native Flask function) or Utilities.raw_sql_to_dict(item) (if you used raw sql to make the query). Once processed, you can send back the data alongside the HTTP code (ex: 200 for success, 500 for server error).

 [App.py] -> Contains the actual route (ie. /get-tools) , the handlers for each type of request (GET,PUT,POST,DELETE), and will pass on the request data to the Handler.
