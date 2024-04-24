from openai import OpenAI
from github import Github

client = OpenAI(api_key = "")
g = Github("")
def get_issue_details(repo_name, issue_number):
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    issue_details = f"Issue: {issue.title}. Issue body: {issue.body}"
    print(issue_details)
    return issue_details

def chat_with_gpt(prompt):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
  )
  return response.choices[0].message.content.strip()

if __name__ == "__main__":
  while True:
    repo_name = "Meski1/Enchatment"
    issue_number = 2
    
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
      break
    if user_input.lower() in ["gitissue"]:
      gitDetails = get_issue_details(repo_name, issue_number)
      response = chat_with_gpt(gitDetails)
      print("Chatbot: ", response)

    
