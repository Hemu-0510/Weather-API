import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("HF_TOKEN not found in .env")
    st.stop()

# Streamlit settings
st.set_page_config(
    page_title="Weather AI Assistant",
    page_icon="🌤️"
)

st.title("🌤️ Weather AI Assistant")
st.write("Ask me about the weather in any city.")


# ---------------------------------------------------
# WEATHER FUNCTION
# ---------------------------------------------------

def get_weather(city):

    try:

        # Find city
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return {
                "error": "City not found"
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location.get("name", city)
        country = location.get("country", "")

        # Get weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "wind_speed_10m",
                "precipitation",
                "weather_code"
            ],
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_data = weather_response.json()

        current = weather_data["current"]

        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Heavy rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail"
        }

        condition = weather_codes.get(
            current.get("weather_code"),
            "Unknown"
        )

        return {
            "city": city_name,
            "country": country,
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "precipitation": current.get("precipitation"),
            "condition": condition
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ---------------------------------------------------
# HUGGING FACE
# ---------------------------------------------------

client = InferenceClient(
    token=HF_TOKEN
)

MODEL = "meta-llama/Llama-3.1-8B-Instruct"


# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

user_input = st.chat_input(
    "Example: What is the weather in Chennai?"
)


if user_input:

    # Show user message

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    try:

        # ------------------------------------------------
        # ASK AI
        # ------------------------------------------------

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a weather assistant. "
                        "If the user asks about weather, "
                        "respond ONLY using this format: "
                        "<function=get_weather>"
                        "{\"city\":\"CITY_NAME\"}"
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],

            max_tokens=100,

            temperature=0.1
        )


        ai_response = response.choices[0].message.content


        # ------------------------------------------------
        # CHECK FOR WEATHER FUNCTION
        # ------------------------------------------------

        if "<function=get_weather>" in ai_response:

            try:

                # Get JSON part

                json_part = ai_response.split(
                    "<function=get_weather>"
                )[1]

                arguments = json.loads(
                    json_part
                )

                city = arguments["city"]


                # ----------------------------------------
                # RUN WEATHER FUNCTION
                # ----------------------------------------

                weather = get_weather(city)


                if "error" in weather:

                    final_answer = (
                        f"Sorry, I could not find weather "
                        f"information for {city}."
                    )

                else:

                    final_answer = (
                        f"### 🌤️ Weather in {weather['city']}, "
                        f"{weather['country']}\n\n"
                        f"**Condition:** {weather['condition']}\n\n"
                        f"**Temperature:** "
                        f"{weather['temperature']} °C\n\n"
                        f"**Feels like:** "
                        f"{weather['feels_like']} °C\n\n"
                        f"**Humidity:** "
                        f"{weather['humidity']}%\n\n"
                        f"**Wind Speed:** "
                        f"{weather['wind_speed']} km/h\n\n"
                        f"**Precipitation:** "
                        f"{weather['precipitation']} mm"
                    )


            except Exception:

                final_answer = (
                    "Sorry, I could not process the "
                    "weather request."
                )

        else:

            final_answer = ai_response


        # ------------------------------------------------
        # SHOW ANSWER
        # ------------------------------------------------

        with st.chat_message("assistant"):

            st.markdown(final_answer)


        st.session_state.messages.append({

            "role": "assistant",

            "content": final_answer

        })


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )