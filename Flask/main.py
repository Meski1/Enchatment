from openai import OpenAI
from github import Github, InputFileContent
from dotenv import load_dotenv
import os

load_dotenv()
openai_key = os.getenv("openai_key")
github_token = os.getenv("githubToken")
conversation_history = []
client = OpenAI(api_key=openai_key)
g = Github(github_token)

last_repo_name = None

def get_issue_details(repo_name, issue_number, conversation_history):
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    issue_details = f"Issue: {issue.title}. Issue body: {issue.body}"

    if conversation_history:
        gist_content = "\n".join([f"{i + 1}. {msg['role']}: {msg['content']}" for i, msg in enumerate(conversation_history)])
        gist = g.get_user().create_gist(public=True, files={f"conversation_{issue_number}.txt": InputFileContent(content=gist_content)})
        issue.create_comment(f"Conversation history: {gist.html_url}")
    
    return issue_details

def select_messages_for_upload(conversation_history):
    print("Conversation History:")
    for i, msg in enumerate(conversation_history):
        print(f"[||{i + 1}||]. {msg['content']}")
    upload_choices = input("Enter the numbers of messages you want to upload (comma-separated): ").split(",")
    upload_indices = [int(choice.strip()) - 1 for choice in upload_choices if choice.strip().isdigit()]
    selected_messages = [conversation_history[i]["content"] for i in upload_indices if 0 <= i < len(conversation_history)]
    return selected_messages

def create_gist_with_selected_messages(conversation_history, repo_name, issue_number):
    if conversation_history:
        selected_messages = select_messages_for_upload(conversation_history)
        file_name = input("Enter the name for the gist text file: ")
        gist_content = "\n".join(selected_messages)
        gist_files = {f"{file_name}.txt": InputFileContent(content=gist_content)}
        gist = g.get_user().create_gist(public=True, files=gist_files)
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(f"Gist URL: {gist.html_url}")
        print("Gist URL:", gist.html_url)
    else:
        print("No conversation history available to create a gist.")

def chat_with_gpt(prompt, upload_last_response=False):
    messages = [
        {"role": "system", "content": "Previous messages:"},
        *conversation_history,
    ]
    if upload_last_response:
        previous_responses = [msg for msg in conversation_history if msg["role"] == "system"]
        messages.extend([
            {"role": "system", "content": f"[||{i + 1}||]. {msg['content']}"} 
            for i, msg in enumerate(previous_responses)
        ])
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    conversation_history = []
    while True:
        user_input = input("You: ").lower()
        if user_input in ["quit", "exit", "bye"]:
            break
        elif user_input == "gitchat":
            if last_repo_name is None:
                repo_name = input("What is the repo name: ")
            else:
                use_last_repo = input(f"Use last repo '{last_repo_name}'? (y/n): ").lower()
                repo_name = last_repo_name if use_last_repo == "y" else input("What is the repo name: ")
            issue_number = int(input("Issue number: "))
            last_repo_name = repo_name
            git_details = get_issue_details(repo_name, issue_number, conversation_history)
            user_input = git_details
            response = chat_with_gpt(user_input)
            print("Chatbot: ", response)
        elif user_input == "gistpush":
            create_gist_with_selected_messages(conversation_history, repo_name, issue_number)
        else:
            response = chat_with_gpt(user_input)
            print("Chatbot: ", response)
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "system", "content": response})
