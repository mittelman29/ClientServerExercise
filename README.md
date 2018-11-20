# Client Server Exercise

The purpose of this exercise is to demonstrate expertise with several technologies and across the web development stack.

## Description
In python, create a script that exposes 2 ports, 11211 and 8000. On the first port, expose a subset of memcached functionality, set, get and delete. On the second port, serve a basic web site that displays the current list of key/value pairs maintained by memcached.

## Requirements

### Backend
1. The Python program must be able to accept multiple connections at once.
2. The data must be persistent, i.e. stored in a database.

### Frontend
1. The web site can be simple, but should use a modern framework.
2. Values should be hidden with JS and only exposed when a user clicks to view.
3. User should be able to add/update/delete key/value pairs.


## Quick Start

1. Clone the repo
```bash
$ git clone https://github.com/mittelman29/ClientServerExercise.git
```

2. Install Memcached
If you're on Mac, run:
```bash
$ brew install memcached
```

  * _For all other OS flavors or for more detailed instructions: https://github.com/memcached/memcached/wiki/Install_

3. Run memcached on port 11311 (default is 11211)
```bash
$ memcached -p 11311 &
```
4. Install prerequisites for data tier
```bash
$ sudo pip install python-binary-memcached
```

5. Install prerequisites for web tier
```bash
$ cd ClientServerExercise/monitoring-site
$ npm i
```

6. Build the React site
```bash
$ npm run build
```

7. Run the service
* You may choose any database name you'd like, but to see sample data populated, use 'database.sqlite'
```bash
$ cd ..
$ python main.py <db_name>
```

8. Happy hacking!
* To view the monitoring site, navigate to http://localhost:8000
* To interact with the data service, navigate to the base url(http://localhost:11211) and use the following url suffixes:

1. **base url** + / => list all key/value pairs
2. **base url** + /**key** => view single key/value pair
3. **base url** + /set?**key**=**value** => create/update a key/value pair
4. **base url** + /del/**key** => delete a key/value pair

## License

This was written for demonstration and educational purposes only and is freely shared with the public. Please feel free to clone, fork or spoon this code as you see fit.

## Disclaimer

This is a work of fiction. Names, characters, businesses, places, events, locales, and incidents are either the products of the author's imagination or used in a fictitious manner. Any resemblance to actual persons, living or dead, or actual events is purely coincidental.