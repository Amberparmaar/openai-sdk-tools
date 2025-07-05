import random
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
import os
from dotenv import load_dotenv
import requests
load_dotenv()

set_tracing_disabled(disabled=True)

GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY')

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

@function_tool()
async def random_jokes():
    """provide a random jokes to user."""
    return random.randint(1, 10)

@function_tool()
async def weather_info(city:str) ->str:
    """you are helping tool , provide weather details according to city name."""
    try:
        result = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
        data = result.json()
        return f'The current weather of {city} is {data["current"]["condition"]["text"]}.'
    except Exception as e:
        return f'could not find weather details due to {e}.'

agent = Agent(
    name='Helping Assistant',
    instructions="""if the user asks for jokes, first call 'random_jokes' function, then tell that jokess with numbers.
if the user asks for weather, call the 'get_weather' funciton with city name""",
    tools=[random_jokes, weather_info],
    model=model
)
prompt= input('Enter your query here: ')
result=Runner.run_sync(agent, prompt)
print(result.final_output)