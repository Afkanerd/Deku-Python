<img src="https://github.com/Afkanerd/Afkanerd-Resources/raw/main/images/Artboard%209.png" align="right" width="350px"/>

# Deku-Python

Afkanerd Deku Python Library

## Installation

Please make sure you have Python 3.7 or newer (python --version).

### Create a Virtual Environments

```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

### PyPI

```bash
$ pip install --upgrade pip wheel
$ pip install "git+https://github.com/Afkanerd/Deku-Python.git@main#egg=DekuPython"
```

Install upgrades

```bash
$ pip install --force-reinstall "git+https://github.com/Afkanerd/Deku-Python.git@main#egg=DekuPython"
```

### From source

```bash
$ git clone https://github.com/Afkanerd/Deku-Python.git
$ cd Deku-Python
$ python3 setup.py install
```

## Usage

```python
import os
import sys
import logging

from DekuPython import Client


def main() -> None:
    """main"""
    account_sid = ""
    auth_token = ""
    connection_url = "localhost"
    pid = ""
    service = "sms"
    operator_code = "62401"
    service_name = Client.get_service_name_from_operator_code(
        pid=pid, service=service, operator_code=operator_code
    )

    def callback(ch_, method, properties, body):
        print(f"[x] Message Received: {body}")
        ch_.basic_ack(delivery_tag=method.delivery_tag)

    try:
        connection, channel = Client.create_channel(
            username=account_sid,
            password=auth_token,
            connection_url=connection_url,
            vhost=account_sid,
            queue_name=service_name,
            exchange_name=pid,
            binding_key=service_name,
            callback=callback,
        )

    except Exception as error:
        raise error

    else:
        try:
            print("[x] Waiting for messages ...")
            channel.start_consuming()

        except Exception as error:
            logging.exception(error)

        finally:
            try:
                channel.close()
                connection.close()
            except Exception as error:
                logging.error(error)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

```

## Licensing

This project is licensed under the [GNU General Public License v3.0](LICENSE).
