### Description

This bot provides a text bridge between an IRC channel and a Mumble server.

### How to install/configure/run

You can directly run vladbot by typing `./run` or `python2 -m vladbot`.
To permanently install vladbot, type `sudo ./setup.py install`. Then, you can run it by typing `vladbot`.

use `./install.sh` for install all Dependencies

You need to provide a config file that (among others) contains user credentials for the bot. An example conf file can be found in `vladbot.conf.example`.

You can either specify a conf file path as a command line argument (`vladbot myconffile.conf`), or place it at `./vladbo.conf` or `/etc/vladbot.conf`.

### Behaviour

By default, the bot

- Relays messages from a mumble channel to an IRC channel
- Leaves the channel when somebody types 'gtfo'
- Tries to reconnect on connection failures

However, this behaviour can be altered easily by editing `vladbot/__main__.py`, which contains several fairly self-explainatory callback functions that will be automatically invoked at the appropriate times.
For example, certain IRC messages may be ignored by adding a line `if message.contains('bannedtext'): return` to the top of `ircTextMessageCallback`.
More complex, 'botty' behaviour may be implemented the same way; note that you can call `irc.sendTextMessage()` and `mumble.sendTextMessage()` from everywhere within the callback functions.

### Dependencies

- python2
- protobuf-python (Debian/Ubuntu/Centos package: python-protobuf, Arch package: python2-protobuf)
- wikiapi wikipedia search
- socli stackover search
- selenium search google webpage

### TODOs

Nice-to-have features (which we don't plan to implement right now, but feel free to do it yourself):

- SSL certificate validation support
- SSL client certificate support
- More chat protocols (e.g. XMPP multi-user chat)
- Init scripts for `<your distribution here>`

### Misc

Mumble uses Google Protobuf for most of its communications; this means that one code file needs to be auto-generated (that's what the `Makefile` is there for). Unfortunately, `protoc` does not officially support `python3`, so we're forced to deal with `python2` and all its string buffer ugliness.

