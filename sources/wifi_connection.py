from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver


WIFI_NAME = "WIFI_NAME"
WIFI_PASSWORD = "WIFI_PASSWORD"


def connect():
    if WIFI_PASSWORD == "WIFI_PASSWORD":
        print("CHANGE WIFI NAME AND PASSWORD VALUES IN SOURCES/WIFI_CONNECTION.PY")
        return False

    wifi_driver.auto_init()

    # tries to establish a connection
    try:
        num_tries = 3
        for i in range(num_tries):
            print("connecting to WIFI... " + str(i+1) + "/" + str(num_tries))
            wifi.link(WIFI_NAME, wifi.WIFI_WPA2, WIFI_PASSWORD)
            print("done")
            return True
        else:
            print("couldn't connect")
            return False
    except Exception as e:
        print("Couldn't connect to WIFI. Error:", e)
        return False


# returns the IP address associated to the device.
def get_ip_address():
    try:
        return wifi.link_info()[0]
    except Exception as e:
        print("Couldn't get IP address. Returning empty string.")
        return ""


# returns wether the device is connected to wifi or not.
def is_connected():
    try:
        return wifi.is_linked()
    except Exception as e:
        print("Couldn't check for existing WIFI connection. Returning false.")
        return False
