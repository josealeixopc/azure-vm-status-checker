import os
from dotenv import load_dotenv

project_folder = os.path.dirname(os.path.realpath(__file__))  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env-vars'))

import azurestatuschecker
app = azurestatuschecker.create_app()

if __name__ == "__main__":
    app.run()