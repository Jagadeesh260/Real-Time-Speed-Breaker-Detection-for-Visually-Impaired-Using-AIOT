import requests
import pickle
import tkinter as tk

# Function to make predictions and display them in the GUI
def predict_and_display():
    global data_array_label
    global prediction_label
    
    try:
        # Send a GET request to the server
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Split the response text into lines based on "<br>"
            lines = response.text.split("<br>")
            
            # Initialize an empty array to store the extracted values
            data_array = []
            
            # Iterate through each line
            for line in lines:
                # Exclude the line containing the prediction message
                if "Prediction:" in line:
                    continue
                
                # Split each line into key and value based on ":"
                parts = line.split(": ")
                if len(parts) == 2:
                    # Extract the value and convert it to float
                    value = float(parts[1])
                    # Append the value to the data array
                    data_array.append(value)
            
            # Print the received data array
            print("Received data array:", data_array)
            
            # Load the pre-trained model from model.pk1
            with open('E:/Practice/HTTP/HTTP_esp32/model.pk1', 'rb') as f:
                model = pickle.load(f)
            
            # Make predictions using the loaded model
            prediction = model.predict([data_array])[0]  # Exclude the last element from data_array
            print("Prediction:", prediction)
            
            # Update GUI labels with received data and prediction
            data_array_label.config(text="Received data array: " + str(data_array))
            
            if prediction == 1:
                prediction_label.config(text="Speed breaker ahead!")
                # Send a POST request to the server with the message
                response = requests.post(speed_breaker_url, data={"message": "Speed breaker ahead!"})
                if response.status_code == 200:
                    print("Message sent to the server successfully.")
                else:
                    print("Failed to send message to the server. Status code:", response.status_code)
                
                # Display the message in the browser
                browser_response = requests.post(speed_breaker_url, data={"message": "Speed breaker ahead! ==> predicted message "})
                if browser_response.status_code == 200:
                    print("Message added successfully in the browser.")
                else:
                    print("Failed to add message in the browser. Status code:", browser_response.status_code)
                
            else:
                prediction_label.config(text="No speed breaker detected.")
            
        else:
            print("Failed to retrieve data from the server. Status code:", response.status_code)
    
    except requests.RequestException as e:
        # Handle any exceptions that may occur during the request
        print("An error occurred:", e)

# Create the Tkinter window
root = tk.Tk()
root.title("ESP32 Data Prediction")

# Create labels to display data and prediction
data_array_label = tk.Label(root, text="Received data array: ")
data_array_label.pack()

prediction_label = tk.Label(root, text="Prediction: ")
prediction_label.pack()

# Button to trigger data fetching, prediction, and display
fetch_button = tk.Button(root, text="Fetch Data and Predict", command=predict_and_display)
fetch_button.pack()

# URL of the ESP32 server
url = 'http://192.168.1.8'
speed_breaker_url = 'http://192.168.1.8/speed-breaker'

# Run the Tkinter event loop
root.mainloop()
