from google.cloud import vision
from google.cloud.vision_v1 import types
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

'''
    This function first reads the content of the image file, 
    creates an instance of the Vision API client, and passes the image content to the web detection method. 
    The web detection method returns a list of web entities associated with the image. 
    If any of the web entities have a description of "Stock photography" or "Royalty-free," 
    it means the image is likely taken from the internet and not original. 
    If no such entities are found, the function returns True, indicating that the image is original.
    '''
def is_original_image(image):
    client = vision.ImageAnnotatorClient()
    with open(image, 'rb') as f:
        content = f.read()
    image = types.Image(content=content)
    response = client.web_detection(image=image)
    if response.web_detection.full_matching_images or response.web_detection.pages_with_matching_images:
        return False
    
    # web_entities = response.web_detection.web_entities
    # for entity in web_entities:
    #     if entity.description == 'Stock photography' or entity.description == 'Royalty-free':
    #         return False
    return True



## Deprecated:
def is_image_from_internet(image_path):
    # Initialize the Vision API client
    # credentials='AIzaSyC96UQIw55-gV4E8gnODYmKY14Yhy0leNw'
    client = vision.ImageAnnotatorClient()

    # Read the image file
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an image object
    image = vision.Image(content=content)

    # Perform a reverse image search
    response = client.image_properties(image=image)
    web_entities = response.web_detection.web_entities

    # Check if the image contains web entities (indicating it is from the internet)
    return len(web_entities) > 0