from flask import current_app as app
import board

try:
    from w1thermsensor import W1ThermSensor
    import adafruit_dht
except Exception:
    W1ThermSensor = None
    adafruit_dht = None


class Sensors:
    @staticmethod
    def get_external_temp():
        """
        Safely read the external temperature
        :return: Integer of current temperature
        """
        app.logger.info("Starting to read temperature sensor")

        try:
            sensor = W1ThermSensor()
            temperature = sensor.get_temperature()
        except TypeError as e:
            app.logger.warning(
                f"Unable to use primary temperature sensor in this environment: {e}"
            )
            temperature = 0
        except Exception as e:
            app.logger.error(
                f"Unknown problem with primary external temperature sensor: {e}"
            )
            temperature = 0

        app.logger.info("Finished reading temperature sensor")
        app.logger.debug(f"Temperature: {temperature}")
        return int(temperature)

    # DHT22 -> sensor
    @staticmethod
    def get_dht_temp():
        """
        Safely read the external temperature from DHT22 sensor
        :return: Integer of current temperature
        """
        app.logger.info("Starting to read DHT22 temperature sensor")

        try:
            dhtDevice = adafruit_dht.DHT22(board.D4)
            temperature_c = dhtDevice.temperature
        except TypeError as e:
            app.logger.warning(
                f"Unable to use primary temperature sensor in this environment: {e}"
            )
            temperature_c = -1
        except Exception as e:
            app.logger.error(
                f"Unknown problem with primary external temperature sensor: {e}"
            )
            temperature_c = -1

        app.logger.info("Finished reading temperature sensor")
        app.logger.debug(f"Temperature: {temperature_c}")
        return int(temperature_c)
