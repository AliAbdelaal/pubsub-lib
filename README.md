# Simple Unified PubSub module

A unified PubSub messaging module that supports Kafka and Google PubSub as backend.

## Installation

### Python environment

You need to clone the repo and create a python3.7 virtualenv as follows.

```bash
$git clone https://github.com/AliAbdelaal/pubsub-lib.git
$cd pubsub-lib/
$python -m venv venv
$source venv/bin/activate
$pip install .
```

### Setup configurations

Create a `configs.json` file for the corresponding backend that you want to use, and set an environment variable with the path of the file as follows.

```bash
$export PUBSUB_CONFIG_PATH='path/to/configs.json'
```

### Kafka installation

![kafka](assets/kafka.png)

To use Kafka as a backend service, you will need to install Kafka, you can follow these blogs to install it.

- [HELLO WORLD IN KAFKA USING PYTHON](https://timber.io/blog/hello-world-in-kafka-using-python/)
- [Kafka-Python explained in 10 lines of code](https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1)
- [Getting started with Apache Kafka in Python](https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05)

Then you will need to setup Kafka configurations file as follows.

- Kafka config file:

    ```json
    {
        "kafka_servers": [
                "localhost:9092"
            ]
    }
    ```

### Google PubSub Installation

![gcp-pubsub](assets/gcp-pubsub.png)

To use Google PubSub you will need to setup a GCP account, create a new PubSub topic and a subscription with a publishing and subscribing permissions.

You can follow [this video](https://youtu.be/f5DOsB7Nlw0) from the creators of Google PubSub to create a topic and a subscription.

You will need to setup the gcp configurations as follows.

- Google PubSub config file:

    ```json
    {
        "type": "YOUR_VALUE_GOES_HERE",
        "project_id": "YOUR_VALUE_GOES_HERE",
        "private_key_id": "YOUR_VALUE_GOES_HERE",
        "private_key": "YOUR_VALUE_GOES_HERE",
        "client_email": "YOUR_VALUE_GOES_HERE",
        "client_id": "YOUR_VALUE_GOES_HERE",
        "auth_uri": "YOUR_VALUE_GOES_HERE",
        "token_uri": "YOUR_VALUE_GOES_HERE",
        "auth_provider_x509_cert_url": "YOUR_VALUE_GOES_HERE",
        "client_x509_cert_url": "YOUR_VALUE_GOES_HERE"
    }
    ```

Then you will need to export two keys as a system environment variables, `GOOGLE_CLOUD_PROJECT` and `GOOGLE_PUBSUB_SUB_ID` which will include the project-ID and the subscription-ID.

```bash
export GOOGLE_CLOUD_PROJECT='PROJECT_ID'
export GOOGLE_PUBSUB_SUB_ID='SUBSCRIPTION_ID'
```

## Usage

The library supports sending and receiving messages in bytes format with an optional string key, here is an example for a producer that sends images to a topic and a consumer that saves these images.

### Producer

> You will need to install Pillow in order to try this example using `pip install Pillow`

```python
# import necessary libs
import io
from PIL import Image
from PubSub import PubSubFactory

# initiate a pubsub object with the backend that you would like to use ['kafka', 'gcp']
pubsub = PubSubFactory('gcp')
# if you have a topic named: images-topic
producer = pubsub.create_producer("images-topic")

try:
    while True:
        # keep on accepting key, value pairs of keys and it's corresponding image path
        key, value = input("enter key, image path:").strip().split(",")
        # read the image and encode it in bytes
        image = Image.open(value)
        with io.BytesIO() as output:
            image.save(output, image.format)
            # send the image via the publisher
            producer.push_msg(output.getvalue(), key=key)
except KeyboardInterrupt:
    print("Okay man, shutting down !")

```

### Consumer

```python
# import libraries
import io
import os
from datetime import datetime
from PIL import Image
from PubSub import PubSubFactory

# Create callback function that accepts key and value
def callback(key:str, value:bytes):
    # create a download file to save the images in
    if not os.path.exists('downloads'):
        os.mkdir("downloads")
    image = Image.open(io.BytesIO(value))
    file_name = f'{datetime.now().isoformat().replace(":", "-").split(".")[0]}.{image.format}'
    # Save the image
    image.save(os.path.join("downloads", file_name))
    print(f"I got an Image !\n\tkey: {key}\n\tsaved to: {file_name}")

# initiate a pubsub object with the backend that you would like to use ['kafka', 'gcp']
pubsub = PubSubFactory('gcp')
# if you have a topic named: images-topic
pubsub.create_consumer("images-topic", callback)
# the consumer will run in a separate thread in the background.
print("A new consumer is running.")
```
