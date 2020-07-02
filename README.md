# fs stats recorder

a simple script i hacked together to watch the fantasy strike `output_log.txt` file and keep track of my ranked performance

**dependencies:**

the following modules are not in the python standard library and must be aquired with pip

- watchgod, for watching the log file
- tabulate, for formatting the table in the output
- paramiko, for pushing the output to a server

python 3.6 features are used, so make sure you're at least that updated

this is currently hardcoded to work on windows but that can be fixed by editing line 10 in `fs_stats.py`, where it reads `OUTPUT_LOG =` etc etc

**setup:**

if you just want to print to a file, i have a tutorial video (i know, i know) for how to set it up https://www.youtube.com/watch?v=_F1m2so6t14

if you want to automatically publish to a server (like i do), set PUBLISH_TO_SERVER to true. put an openssh private key file in the same folder as where you cloned this to that can be used to connect to your server. then go to the bottom of `database.py` and change the hostname and username to the ones relevant for your server. (mine are weird because my personal site is hosted on the same server as my mastodon instance. don't worry about it.)

this was originally meant just for me, so apologies for the user unfriendliness. maybe one day i'll get around to making it properly configurable