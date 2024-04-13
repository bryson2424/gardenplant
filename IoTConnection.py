import IOinfo
from Plant import Plant
from Adafruit_IO import Client, MQTTClient, Feed
import base64
from io import BytesIO
from PIL import Image
import firebaseStorage
from datetime import datetime

class IoTConnection():
    """Helps facilitate a connection to Adafruit IO for uploading data
    """
    def __init__(self):
        self.username = IOinfo.username
        self.key = IOinfo.key

        self.client = Client(self.username, self.key)
        self.mqttClient = MQTTClient(self.username, self.key)
        self.mqttClient.connect()

    def createFeed(self, plant):
        """Creates a new Adafruit IO feed for a given plant, if it does not
        already exist.

        :param plant: Plant class
        :return: None
        """

        if not self.__feedExists(plant.name):
            imageFeed = Feed(name=plant.name+'_image', history=False)
            tempFeed = Feed(name=plant.name+'_temp')
            moistureFeed = Feed(name=plant.name+'_moisture')

            self.client.create_feed(imageFeed)
            self.client.create_feed(tempFeed)
            self.client.create_feed(moistureFeed)

    def uploadData(self, plant, data):
        """Upload a dictionary of plant data to Adafruit IO and Firebase Storage

        :param plant:
        :param data:
            Contains {base64Image: data, temp: data, moisture: data}
        :return:
        """
        print(plant.imageKey, plant.tempKey, plant.moistureKey)

        if len(data["base64Image"]) > 102400:
            print("WARNING: Image resolution too large to upload to Adafruit IO")
        else:
            # Safely upload image to firebase
            now = datetime.now()

            current_time = now.strftime("%m_%d_%y-%H_%M_%S")

            img = Image.open(BytesIO(base64.b64decode(data["base64Image"])))
            img.save("{}_{}.png".format(plant.name,current_time), format="PNG", optimize=True, quality=85)
            firebaseStorage.uploadImageToFirebaes("{}_{}.png".format(plant.name, current_time))

        self.mqttClient.publish(plant.imageKey, data["base64Image"])
        self.client.send(plant.tempKey, data["temp"])
        self.client.send(plant.moistureKey, data["moisture"])

    def convertImageFileToBase64(self, fileName, fileType="PNG"):
        """ Converts a given filepath to Base64 encoding

        :param fileName:
        :param fileType: the path to the file, including filename
        :return: base64 image byte data
        """
        img = Image.open(fileName)
        im_file = BytesIO()
        img = img.resize((300,225), Image.LANCZOS)
        img.save(im_file, format=fileType, optimize=True, quality=85)
        im_bytes = im_file.getvalue()
        im_b64 = base64.b64encode(im_bytes)

        return im_b64

    def __feedExists(self, feedName):
        feedNames = []

        for feed in self.client.feeds():
            print(feed)
            if feed.name not in feedNames:
                feedNames.append(feed.name)

        if (feedName+'_temp' in feedNames) or (feedName+'_image' in feedNames) or (feedName+'_moisture' in feedNames):
            return True
        else:
            return False


conn = IoTConnection()

p = Plant("mob")

conn.createFeed(p)


im_b64 = conn.convertImageFileToBase64("Street_Pic.jpg", fileType="JPEG")

data = {"base64Image": im_b64, "temp": 74, "moisture": 500}

conn.uploadData(p, data)