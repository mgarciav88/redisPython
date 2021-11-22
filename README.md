## POC redis + flask + multiprocessing

To test this small project, redis needs to be installed locally. 
Follow [redis installation guide](https://redis.io/topics/quickstart). The project assumes all defaults are set, 
there is no need for special configuration.

To install python dependencies run:

```bash
pipenv install
```

The main external library used is the [redis client](https://pypi.org/project/redis/) recommended by the redis team.

The src includes two basic scripts:
* app
* main

Running 

```bash
python src/app.py
```

Starts the flask app on local host port 81 with a single endpoint "/".

When running this endpoint, the producer and consumer processes push to a redis list with key defined in src.constants.
The list will keep growing each time the endpoint is run.

On the other hand, running:

```bash
python src/read.py
```

Runs the reader process which pops all the data from the redis list with key "Counter". After main is run, the list is 
left empty.


