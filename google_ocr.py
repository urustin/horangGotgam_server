
# import argparse 
# import google
from google.cloud import vision
from google.oauth2 import service_account


def detect_text(path):
    """Detects text in the file."""
    
    key_file_path = './haranggotgam-22ece62e15d4.json'
    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    credentials = service_account.Credentials.from_service_account_file(key_file_path, scopes=scopes)

    # Use the credentials with the Vision API client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    texts = response.text_annotations
    print("Texts:")
    return (texts[0].description)
    # print(texts[0].description)
    # for text in texts:
    #     print(f'\n"{text.description}"')

    #     vertices = [
    #         f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
    #     ]

    #     print("bounds: {}".format(",".join(vertices)))

    
# detect_text("./1.jpeg")