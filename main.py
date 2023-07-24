import os
import discord
import json
import requests

API_URL = 'https://api-inference.huggingface.co/models/TejasC2/'


class MyClient(discord.Client):

  def __init__(self, model_name):
    intents = discord.Intents.default(
    )  
    intents.message_content = True
    super().__init__(intents=intents)
    self.api_endpoint = API_URL + model_name
    huggingface_token = os.environ['HUGGINGFACE_TOKEN']
    self.request_headers = {
        'Authorization': 'Bearer {}'.format(huggingface_token)
    }

  def query(self, payload):
    """
        make request to the Hugging Face model API
        """
    data = json.dumps(payload)
    response = requests.request('POST',
                                self.api_endpoint,
                                headers=self.request_headers,
                                data=data)
    ret = json.loads(response.content.decode('utf-8'))
    return ret

  async def on_ready(self):
    print('Logged in as')
    print(self.user.name)
    print(self.user.id)
    print('------')

    self.query({'inputs': {'text': 'Hello!'}})

  async def on_message(self, message):
    """
        this function is called whenever the bot sees a message in a channel
        """
    if message.author.id == self.user.id:
      return

    payload = {'inputs': {'text': message.content}}

    async with message.channel.typing():
      response = self.query(payload)
    bot_response = response.get('generated_text', None)

    if not bot_response:
      if 'error' in response:
        bot_response = '`Error: {}`'.format(response['error'])
      else:
        bot_response = 'Hmm... something is not right.'

    await message.channel.send(bot_response)


def main():
  client = MyClient('DialoGPT-TejasBot')
  client.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
  main()
