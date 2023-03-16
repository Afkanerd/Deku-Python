"""Deku Python Library"""

import logging
import pika

from DekuPython.std_carrier_lib.helpers import CarrierInformation

logger = logging.getLogger(__name__)


class Client:
    """Deku Python Client"""

    @staticmethod
    def get_service_name_from_operator_code(
        pid: str,
        service: str,
        operator_code: str = None,
    ) -> str:
        """Get Service name from identifier

        Keyword arguments:
        pid -- project's ID
        operator_code -- Got from modem

        return: str
        """

        ci_ = CarrierInformation()

        try:
            if service.lower() in ["sms"]:
                country_name = ci_.get_country(operator_code=operator_code)
                service_provider = ci_.get_operator_name(operator_code=operator_code)
                service_name = f"{pid}_{country_name}_{service_provider}"

        except Exception as error:
            raise error

        else:
            logger.info("[X] Successful!")

            return service_name

    @staticmethod
    def create_channel(
        username,
        password,
        connection_url,
        queue_name,
        exchange_name,
        binding_key,
        vhost,
        connection_name="sample_connection_name",
        durable=True,
        callback=None,
        prefetch_count=1,
        connection_port=5672,
        heartbeat=30,
    ) -> None:
        """Create a RabbitMQ channel"""

        credentials = pika.PlainCredentials(username, password)
        try:
            client_properties = {"connection_name": connection_name}

            parameters = pika.ConnectionParameters(
                host=connection_url,
                port=connection_port,
                virtual_host=vhost,
                credentials=credentials,
                heartbeat=heartbeat,
                client_properties=client_properties,
            )

            connection = pika.BlockingConnection(parameters=parameters)
            channel = connection.channel()
            try:
                channel.exchange_declare(
                    exchange=exchange_name,
                    durable=True,
                    passive=True,
                )

            except pika.exceptions.ChannelClosedByBroker as error:
                if (str(error)[1:4]) == "404":
                    logger.exception(str(error))
                    raise error

            channel.queue_declare(queue_name, durable=durable)
            channel.basic_qos(prefetch_count=prefetch_count)

            if binding_key is not None:
                channel.queue_bind(
                    exchange=exchange_name, queue=queue_name, routing_key=binding_key
                )

            if callback is not None:
                channel.basic_consume(queue=queue_name, on_message_callback=callback)

            return connection, channel

        except pika.exceptions.AMQPConnectionError as error:
            raise error

        except Exception as error:
            raise error
