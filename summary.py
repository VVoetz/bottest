from openai import OpenAI
client = OpenAI()
input = input("gpt prompt?:")
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  max_tokens=50,
  messages=[
    {"role": "system", "content": f"{input}"}
  ]
)

print(completion.choices[0].message.content)

