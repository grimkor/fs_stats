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

put an openssh private key file in the same folder as where you cloned this to that can be used to connect to your server. then go to line 143 in `database.py` and change the hostname and username to the ones relevant for your server. (mine are weird because my personal site is hosted on the same server as my mastodon instance. don't worry about it.) while you're there, you can customize the output by modifying the lines just above that in the `publish()` function

then just make sure that `fs_stats.py` is running when you open the game