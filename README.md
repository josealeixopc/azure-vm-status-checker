# azure-vm-status-checker

A simple Python server with authentication for retrieving whether a process is running in an Azure VM port not. If it is not, it sends a request to start the VM. Applied to a Minecraft server process, to reduce VM usage.

Suggestions or improvements to the project and its structure are welcome!

## References

- [DigitalOcean - How To Add Authentication to Your App with Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)
- [Azure docs - Automation VM Management](https://docs.microsoft.com/pt-pt/azure/automation/automation-solution-vm-management)

## Prerequisites

- Azure Webhook URL (for starting the VM).

### Creating the Azure Webhook

1. Create an Azure Automation account
1. Create a runbook that stops Azure VMs
    - In my case, I searched the runbook gallery and chose the `Start Azure V2 VMs` by the Azure team.
1. Create a webhook for the runbook with the appropriate parameters.
1. Set the `AZURE_MC_START_WEBHOOK_URL` variable to the runbook URL.

## Installing

### Flask-SQLAlchemy usage

Flask-SQLAlchemy is a package for using SQLAlchemy within a Flask application.

#### Adding a row to the database

Flask provides a very useful Shell utility, which let's us run Python code inside the context of the Flask app.

After making sure that the application is running using `flask run`, export the Flask app and attachthe Flask shell:

```bash
export FLASK_APP=app.py
flask shell
```

Then, add an `azurestatuschekcer.models.Admin` row:

```python
from azurestatuschecker import db
from azurestatuschecker.models import Admin
from werkzeug.security import generate_password_hash

admin=Admin(username='admin', password=generate_password_hash('password', method='sha256')) # you can hash the password if you want

db.session.add(admin)
db.session.new  # verify what are the new rows
db.session.commit()

Admin.query.all() # should return the row you just inserted

# Admin.query.delete() # deletes all the rows in the Admin table and returns the number of rows deleted
```
## Running

Before running the app, you must set some environment variables. You can do so either by exporting them or by renaming the `.env-vars.example` file to `.env-vars` and filling the value for the variables:

```bash
export AZURE_MC_START_WEBHOOK_URL=<url_to_azure_webhook>
export SERVER_IP_ADDRESS=<server_ip>
```

## Deploying

### To Heroku

To deploy the application, you must first create the Heroku Dyno and add the Heroku Postgres Add-On. Then, on the project's root directory:

```bash
heroku login
heroku git:remote -a <heroku-app-name>
git push heroku master
```

To add an admin credential to the database do:

```bash
heroku run bash
flask shell
```

And then copy the code in the ["adding a row" section](#adding-a-row-to-the-database) and `exit()` the Python REPL and `exit` the Heroku `bash`.

## Developing

Running a development instance:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Running PostgreSQL on Docker

To start the container: 

```bash
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres 
```

The container exposes the port `5432`, so we connect to it (you may need to install the PSQL client):

```bash
psql -h localhost -p 5432 -U postgres
```

## Contributors

-[José Aleixo Cruz](https://github.com/josealeixopc)