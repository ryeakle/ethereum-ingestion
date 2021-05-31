# Instructions: create a settings.py file in this directory and update these values
# infura_client/settings.py is gitignored, but always double check to make sure you aren't committing
# any secrets to version control

# Infura credentials
INFURA_PROJECT_ID = "your infura project id"

# infura settings
INFURA_WEBSOCKET = f"wss://mainnet.infura.io/ws/v3/{INFURA_PROJECT_ID}"
INFURA_SUBSCRIPTION = "newHeads"  # could be one of many subscription types (https://infura.io/docs/ethereum/wss/eth-subscribe)

# kafka settings
KAFKA_SERVER = ["kafka:9092"]  # use this to connect from the infura_client container
KAFKA_SERVER_LOCAL = ["127.0.0.1:9093"]  # use this to connect from the host machine
KAFKA_TOPIC = "infura"
