import cv2
import threading
import base64
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

class camThread(threading.Thread):
    def __init__(self, previewName, camID, base64Image = "", flag = 0):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.base64Image = base64Image
        self.flag = flag
    def run(self):
        print ("Starting " + self.previewName)
        self.webcamView()
        print("Running the AI...")
        print("Printing Base64q")
        response = plantgpt(self.base64Image)
        print("Response Finally")
        print(response)
        
    def webcamView(self):
        cv2.namedWindow(self.previewName)
        cam = cv2.VideoCapture(self.camID)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        if cam.isOpened():  # try to get the first frame
            rval, frame = cam.read()
        else:
            rval = False

        while rval:
            cv2.imshow(self.previewName, frame)
            rval, frame = cam.read()
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord('q'):
                break

            if pressedKey == ord('p'):            
                rval, frame = cv2.imencode('.png', frame)
                self.base64Image = base64.b64encode(frame).decode('utf-8')
    #             retval1, buffer2 = cv2.imencode('.png', image2)
    #             jpg_as_text2 = base64.b64encode(buffer2)
                print(self.previewName)
                print(self.base64Image)
#     #             print(jpg_as_text2)
                break
        cam.release()
        cv2.destroyAllWindows()
        self.flag = 1
#         return jpg_as_text

def plantgpt(base64_image):
    client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

    # def encode_image(image_path):
    #   with open(image_path, "rb") as image_file:
    #     return base64.b64encode(image_file.read()).decode('utf-8')

    completion = client.chat.completions.create(
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Your role is to 1) identify the plant with JUST THE NAME OF THE PLANT, nothing else.. then, output '0' if the plant does not need watering, and '1' if the plant needs watering. then, output '0' if the plant has no bugs and '1' if the plant has bugs. Here is an image."},
            {
              "type": "image_url",
              "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
          ],
        }
      ],
      model="gpt-4-turbo" 
    )

    print(completion.choices[0].message.content)
#     return(

thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 3)
thread1.start()
thread2.start()

if(thread1.flag == 1):
    print("Running the AI...")
    print("Printing Base64q")

print("Printing Base64q")
print(thread1.base64Image)







