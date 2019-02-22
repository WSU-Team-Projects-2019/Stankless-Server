# Stankless-Server
Server Logic for use with the Stankless TrashCAN


### Setting Up Flask

You will need Python 3 to set up Flask properly. You may also need to install the Python 3 virtual environment package with `sudo apt install python3-venv`.

Set up a python virtual environment and activate it. After that, install Flask itself:

```
python3 -m venv venv
. venv/bin/activate
pip install flask
```

Specify the location of the flask app (the file `server.py`) and export it. To do this, open `~/.bashrc` and add the following to the bottom of the file:

```
export FLASK_APP=path/to/server.py
source ~/.bashrc
```

Replacing `path/to/server.py` to wherever the actual file is. The flask server can now be run with `flask run`.
