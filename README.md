# The Rogue - Florida Man Headline Generator

# Team Members:
* [Kalen Shamy](https://github.com/kalenshamy)
* [Jehoon (Jamie) Ryu](https://github.com/mijnap1)
* [Michael Huang](https://github.com/astoppop)
* [Emily Kim-Vance](https://github.com/Orville1415)
* [Parker Kline](https://github.com/ParkerKline)
* [Ria Gulati](https://github.com/RiaGulati)

# Server Setup Instructions

cd into the `/app` folder

Run `python3 -m pip install -r requirements.txt` to download the libraries needed by the application.

You'll want to edit [line 408](/app/main.py#L408) of the `main.py` file if using a production WSGI server to host the web app, and change `website_url ` to the URL or IP address of the WSGI server.

You'll want to edit [line 409](/app/main.py#L409) of the `main.py` file if using a production WSGI server to host the web app, and is configured to host through HTTPS, and set `is_https` variable to `True`.

You'll want to open `model/gdrive.txt`, and download the files at the google drive links to the `model` folder.

From there, run `python3 -m main` to start the server on local, most changes while developing will be picked up in realtime by the server. Note that upon cloning this repository an example project with an untrained model will show up upon running `python3 -m main`.
