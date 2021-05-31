
## About
A quick project for streaming ethereum node messages from an Infura project to a Kafka server running on a container. Provisions the bitnami kafka server (https://hub.docker.com/r/bitnami/kafka/) and an Infura websocket client app container defined under `infura_client/` which tries to connect to your project, then pipes messages to the kafka server under whichever topic you specify using a python executable.


## How To

### Provision the stack
1. Create a project on Infura (free for under 100k requests per day)
2. set the appropriate values in `infura_client/settings.py` for pointing the container to your Infura project and whichever kafka topic you'd like to stream to. _Do not commit any secret info to version control_
3. provision with `docker-compose up -d` in the project root directory
4. confirm everything is working as expected with `docker ps -a`. This stack does a tiny bit of error handling on startup, but things can always go wrong.
5. Later when you're done, you can spin down the stack with `docker-compose down`

### Read messages in a python program
1. Highly recommend setting up a virtualenv for this using the tool of your choice
2. run `pip install -r requirements.txt` from the project root
3. run `ipython` and connect to the kafka server and begin streaming in messages like:
```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
	"<topic name you set up in infura_client/settings.py>",
	bootstrap_servers=["127.0.0.1:9093"]
)

for message in consumer:
	print(message)
```
4. besides this local python consumer, you can connect up whatever other consumers you might want to use for this Kafka server!

## References
https://hub.docker.com/r/bitnami/kafka/
https://infura.io/docs/ethereum/wss/eth-subscribe
