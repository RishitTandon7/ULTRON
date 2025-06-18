import cv2
from PIL import Image
import ollama
import threading

# Function to display the image using PIL
def display_image(image_path):
    img = Image.open(image_path)
    img.show()

# Function to capture the image and process the query
def process_image(query):
    # Open webcam
    cap = cv2.VideoCapture(0)

    # Capture frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        cap.release()
        return "Failed to capture image."

    else:
        # Save the current frame as an image
        image_path = 'current_frame.jpg'
        cv2.imwrite(image_path, frame)

        # Display the captured frame in a separate thread
        image_thread = threading.Thread(target=display_image, args=(image_path,))
        image_thread.start()

        # Send the image and the query to the model
        try:
            response = ollama.chat(
                model='llama3.2-vision',
                messages=[{
                    'role': 'user',
                    'content': query,
                    'images': [image_path]
                }]
            )

            # Return the model response
            return response['message']['content']
        
        except Exception as e:
            print(f"Error while calling the model: {e}")
            return "Failed to get a response from the model."

        finally:
            # Release the webcam
            cap.release()

