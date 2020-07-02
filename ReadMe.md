Create virtual environment folder to install all the required packages for the project: python -m venv venv (<the folder name>)
run the virtual environment: venv\Scripts\activate
To install the libraries needed
to create a file with with packages to install: pip freeze > requirements.txt
to install all the packages from the requirements.txt: pip install -r requirements.txt