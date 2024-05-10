from flask import Flask, render_template, request
from main import chat_with_gpt, get_issue_details, create_gist_with_selected_messages, conversation_history

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    global conversation_history  # Ensure you are referring to the global variable
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.lower() in ["quit", "exit", "bye"]:
            return "Goodbye!"
        elif user_input.lower() == "gitchat":
            repo_name = request.form.get('repo_name', '')
            issue_number = int(request.form.get('issue_number', 0))
            git_details = get_issue_details(repo_name, issue_number, conversation_history)
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "system", "content": git_details})
            return render_template('home.html', conversation_history=conversation_history)
        elif user_input.lower() == "gistpush":
            repo_name = request.form.get('repo_name', '')
            issue_number = int(request.form.get('issue_number', 0))
            create_gist_with_selected_messages(conversation_history, repo_name, issue_number)
            return "Gist URL created!"
        else:
            response = chat_with_gpt(user_input, conversation_history)
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "system", "content": response})
            return render_template('home.html', conversation_history=conversation_history)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
