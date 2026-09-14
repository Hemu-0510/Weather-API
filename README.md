# Weather AI Assistant

## Overview

Weather AI Assistant is an AI-powered Streamlit application that provides real-time weather information using natural language queries.

The application uses an AI model to understand the user's question, perform a weather function call, and retrieve current weather data from the Open-Meteo API.

## Features

* Natural language weather queries
* AI function calling
* Real-time weather information
* Temperature and feels-like temperature
* Humidity
* Wind speed
* Precipitation
* Weather condition
* Interactive Streamlit interface

## Technologies Used

* Python
* Streamlit
* Hugging Face
* Llama 3.1
* Open-Meteo API
* Requests
* Python-dotenv

## How It Works

```text
User Question
      |
      v
AI Model
      |
      v
Weather Function
      |
      v
Open-Meteo API
      |
      v
Weather Result
```

The AI identifies the city from the user's question and calls the `get_weather()` Python function. The function retrieves the current weather data from the Open-Meteo API and displays it in the application.



```

## Output

The application provides real-time weather information through a simple conversational interface.

<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/481fa8da-dd8b-4711-bb8e-e5d4e8d241cc" />




## Conclusion

Weather AI Assistant demonstrates how AI, Python functions, and external APIs can work together to create a practical real-time application. The project provides hands-on experience in AI integration, function calling, API communication, and Streamlit development.
