import requests
import pickle
import tkinter as tk
from tkinter import font as tkfont


class SpeedBreakerDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Breaker Detection")

        # Main frame for the GUI elements
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Title at the top with centered alignment
        title_label = tk.Label(
            self.main_frame,
            text="Speed Breaker Detection",
            font=("Times New Roman", 18, "bold"),
            justify="center",
            borderwidth=0,
            relief="flat",
        )
        title_label.pack(pady=10)

        # Font and width configuration for consistent label styles
        label_font = ("Times New Roman", 16, "bold")
        label_width = 30

        # Labels for the data points
        self.speed_label = tk.Label(
            self.main_frame,
            text="Speed: N/A",
            anchor="center",
            justify="center",
            font=label_font,
            width=label_width,
            height=2,
            borderwidth=0,
            relief="flat",
        )
        self.speed_label.pack(pady=5)

        self.latitude_label = tk.Label(
            self.main_frame,
            text="Latitude: N/A",
            anchor="center",
            justify="center",
            font=label_font,
            width=label_width,
            height=2,
            borderwidth=0,
            relief="flat",
        )
        self.latitude_label.pack(pady=5)

        self.longitude_label = tk.Label(
            self.main_frame,
            text="Longitude: N/A",
            anchor="center",
            justify="center",
            font=label_font,
            width=label_width,
            height=2,
            borderwidth=0,
            relief="flat",
        )
        self.longitude_label.pack(pady=5)

        self.change_label = tk.Label(
            self.main_frame,
            text="Change: N/A",
            anchor="center",
            justify="center",
            font=label_font,
            width=label_width,
            height=2,
            borderwidth=0,
            relief="flat",
        )
        self.change_label.pack(pady=5)

        # Prediction label
        self.prediction_label = tk.Label(
            self.main_frame,
            text="Prediction: N/A",
            anchor="center",
            justify="center",
            font=("Times New Roman", 16, "bold"),
            width=label_width,
            height=3,
            borderwidth=0,
            relief="flat",
        )
        self.prediction_label.pack(pady=10)

        # Button to trigger data fetching and prediction
        self.fetch_button = tk.Button(
            self.main_frame,
            text="Fetch Data and Predict",
            command=self.fetch_and_predict,
        )
        self.fetch_button.pack(pady=10)

    # Function to fetch data and make predictions
    def fetch_and_predict(self):
        try:
            # URL of the ESP32 server
            url = 'http://192.168.1.2'
            speed_breaker_url = 'http://192.168.1.2/speed-breaker'
            
            response = requests.get(url)
            
            if response.status_code == 200:
                # Extract data and update labels
                lines = response.text.split("<br>")
                data_array = []
                for line in lines:
                    if "Prediction:" in line:
                        continue  # Skip prediction
                
                    parts = line.split(": ")
                    if len(parts) == 2:
                        value = float(parts[1])
                        data_array.append(value)

                if len(data_array) >= 4:
                    speed, latitude, longitude, change = data_array

                    # Update GUI labels with the received data
                    self.speed_label.config(text=f"Speed: {speed:.2f}")
                    self.latitude_label.config(text=f"Latitude: {latitude:.2f}")
                    self.longitude_label.config(text=f"Longitude: {longitude:.2f}")
                    self.change_label.config(text=f"Change: {change:.2f}")

                    # Load the pre-trained model and make a prediction
                    with open('E:/Practice/HTTP/HTTP_esp32/model.pk1', 'rb') as f:
                        model = pickle.load(f)

                    prediction = model.predict([data_array])[0]

                    if prediction == 1:
                        # Update prediction label
                        self.prediction_label.config(text="Speed breaker ahead!")

                        # Send POST request to trigger LED blink
                        led_url = 'http://192.168.1.2/led-blink'
                        led_response = requests.post(led_url, data={"command": "blink"})
                        if led_response.status_code == 200:
                            print("LED blink command sent successfully.")
                        else:
                            print("Failed to send LED blink command. Status code:", led_response.status_code)

                        # Send POST request to server with the message
                        message_response = requests.post(speed_breaker_url, data={"message": "Speed breaker ahead!"})
                        if message_response.status_code == 200:
                            print("Message sent to the server successfully.")
                        else:
                            print("Failed to send message to the server. Status code:", message_response.status_code)

                        # Display the message in a browser or another interface
                        browser_response = requests.post(speed_breaker_url, data={"message": "Speed breaker ahead! ==> predicted message "})
                        if browser_response.status_code == 200:
                            print("Message added successfully to the browser.")
                        else:
                            print("Failed to add message to the browser. Status code:", browser_response.status_code)

                    else:
                        self.prediction_label.config(text="No speed breaker detected.")

                else:
                    print("Failed to retrieve enough data from the server.")

            else:
                print("Failed to retrieve data from the server. Status code:", response.status_code)

        except requests.RequestException as e:
            print("An error occurred:", e)


# Create the Tkinter window and instantiate the app
root = tk.Tk()
app = SpeedBreakerDetectionApp(root)

# Run the Tkinter event loop
root.mainloop()
