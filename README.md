# The Rogue - Florida Man Headline Generator - Kalen's Fork

gonna be working a little more on this when i have more free time. check back for updates!

# Server Setup instructions

cd into the `/app` folder

Run `python3 -m pip install -r requirements.txt` to download the libraries needed by the application.

You'll want to edit [line 408](/app/main.py#L408) of the `main.py` file if using a production WSGI server to host the web app, and change `website_url ` to the URL or IP address of the WSGI server.

You'll want to edit [line 409](/app/main.py#L409) of the `main.py` file if using a production WSGI server to host the web app, and is configured to host through HTTPS, and set `is_https` variable to `True`.

You'll want to open `model/gdrive.txt`, and download the files at the google drive links to the `model` folder.

From there, run `python3 -m main` to start the server on local, most changes while developing will be picked up in realtime by the server. Note that upon cloning this repository an example project with an untrained model will show up upon running `python3 -m main`.


# Update Log
## V0
[V0.0](https://github.com/KalenShamy/SC22-BatchD-CellarRogues/tree/fc43e0129fa2c70ca03f2049cceb546fe19a0708) - Forked Repo from [hghamblin/SC22-BatchD-CellarRogues](https://github.com/hghamblin/SC22-BatchD-CellarRogues) and Created New README File - (8/26/2022)
V0.1 - Removed useless hidden files, clearer & easy setup - (8/30/2022)
