                    speak("What would you like to ask about the image?")
                        query = take_command().lower()  # Get voice input from the user

                        speak("Sure, capturing the image now.")
                        
                        # Directly call process_image and get the response
                        model_response = process_image(query)
                        
                        # Speak the model's response
                        speak(f"The model says: {model_response}")

