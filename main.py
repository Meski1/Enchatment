import openai

openai.api_key = ""
def chat_with_gpt(prompt):
  response = openai.ChatCompletion.create(
    model="",
    messages=[{"role": "user", "content": prompt}]
  )
  return response.choices[0].message.content.strip()

if _name_ == "_main_":
  while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
      break

  response = chat_with_gpt(user_input)
  print("Chatbot: ", response)