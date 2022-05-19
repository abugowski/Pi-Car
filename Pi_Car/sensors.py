from flask import current_app as app

# import board
from gpiozero import Button, exc

try:
    from w1thermsensor import W1ThermSensor

    # import adafruit_dht
except Exception:
    W1ThermSensor = None
    # adafruit_dht = None


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
    # @staticmethod
    # def get_dht_temp():
    #     """
    #     Safely read the external temperature from DHT22 sensor
    #     :return: Integer of current temperature
    #     """
    #     app.logger.info("Starting to read DHT22 temperature sensor")
    #
    #     try:
    #         dhtDevice = adafruit_dht.DHT22(board.D17, False)
    #         temperature_dht = dhtDevice.temperature
    #     except TypeError as e:
    #         app.logger.warning(
    #             f"Unable to use DHT temperature sensor in this environment: {e}"
    #         )
    #         temperature_dht = -1
    #     except Exception as e:
    #         app.logger.error(
    #             f"Unknown problem with primary external temperature sensor: {e}"
    #         )
    #         temperature_dht = -1
    #
    #     app.logger.info("Finished reading temperature sensor")
    #     app.logger.debug(f"Temperature: {temperature_dht}")
    #     return int(temperature_dht)

    @staticmethod
    def get_boot_status():
        """
        Safely read the boot sensor and calculate the state - open/closed/unknow
        :return: String - boot status
        """
        app.logger.info("Starting to read boot sensor")
        result = None
        status = None

        try:
            button = Button(pin=14)
            status = button.is_pressed
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use boot sensor in this environment: {e}")
            result = "Unknown"
        except Exception as e:
            app.logger.error(f"Unknown problem with boot sensor: {e}")
            result = "Unknown"

        if not result:
            if status:
                result = "Closed"
            else:
                result = "Open"

        app.logger.debug(f"Boot: {result}")
        app.logger.info("Finished reading boot sensor")
        return result
