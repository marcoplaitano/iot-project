from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver


WIFI_NAME = "WIFI_NAME"
WIFI_PASSWORD = "WIFI_PASSWORD"


def connect():
    """
    Connects the board to the wifi.
    """
    if WIFI_PASSWORD == "WIFI_PASSWORD":
        print("CHANGE WIFI NAME AND PASSWORD VALUES IN SOURCES/WIFI_CONNECTION.PY")
        return False

    wifi_driver.auto_init()

    try:
        num_tries = 3
        for i in range(num_tries):
            print("connecting to WIFI... " + str(i+1) + "/" + str(num_tries))
            wifi.link(WIFI_NAME, wifi.WIFI_WPA2, WIFI_PASSWORD)
            print("done")
            return True
        else:
            print("Could not connect.")
            return False
    except Exception as e:
        print("Could not connect to WIFI. Error:", e)
        return False


def get_ip_address():
    """
    Returns the IP address associated to the device.
    """
    try:
        return wifi.link_info()[0]
    except Exception as e:
        print("Could not get IP address. Returning empty string.")
        return ""


def is_connected():
    """
    Returns wether the device is connected to wifi or not.
    """
    try:
        return wifi.is_linked()
    except Exception as e:
        print("Could not check for existing WIFI connection. Returning false.")
        return False
