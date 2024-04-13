from firebase_admin import credentials, initialize_app, storage
# Init firebase with your credentials
cred = credentials.Certificate("servicekey.json")
initialize_app(cred, {'storageBucket': 'gardenplant-71736.appspot.com'})


def uploadImageToFirebaes(image):
    fileName = image
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    print("your file url", blob.public_url)