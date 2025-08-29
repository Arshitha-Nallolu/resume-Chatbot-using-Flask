from flask import Flask, render_template_string, request, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Example skills list
required_skills = ["Python", "Machine Learning", "SQL", "Web Development", "Data Analysis", "Git"]

# Chatbot response function
def chatbot_response(user_input):
    user_input = user_input.lower()

    if "skills present" in user_input:
        return f"✅ Skills present: {', '.join(required_skills[:3])}"

    elif "skills missing" in user_input:
        return f"❌ Skills missing: {', '.join(required_skills[3:])}"

    elif "summary" in user_input:
        return "📝 Your resume highlights Python, Machine Learning, SQL, and Web Development with relevant projects."

    elif "improve" in user_input:
        return "💡 You can improve by adding more certifications and hands-on projects."

    elif "certifications" in user_input:
        return "🎓 No certifications were found in your resume. Consider adding relevant ones."

    else:
        return "🤖 I can help with: skills present, skills missing, summary, certifications, improvements."

# HTML template
html_template = """ 
<!DOCTYPE html>
<html>
<head>
    <title>Resume Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; background: #ece5dd; display: flex; justify-content: center; align-items: center; height: 100vh; }
        #chat-container { width: 400px; height: 600px; background: #fff; border-radius: 10px; display: flex; flex-direction: column; box-shadow: 0px 4px 6px rgba(0,0,0,0.2); }
        #chatbox { flex: 1; padding: 10px; overflow-y: auto; display: flex; flex-direction: column; }
        .message { margin: 8px 0; padding: 10px; border-radius: 8px; max-width: 70%; }
        .user { background: #dcf8c6; align-self: flex-end; }
        .bot { background: #f1f0f0; align-self: flex-start; }
        form { display: flex; border-top: 1px solid #ddd; margin-top: 5px; }
        input[type=text] { flex: 1; padding: 10px; border: none; outline: none; }
        button { padding: 10px; border: none; background: #128C7E; color: white; cursor: pointer; }
        button:hover { background: #075E54; }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="chatbox">
            {% if chat %}
                {% for role, text in chat %}
                    <div class="message {{ role }}">{{ text|safe }}</div>
                {% endfor %}
            {% endif %}
        </div>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="resume">
            <button type="submit">Upload Resume</button>
        </form>
        <form method="POST">
            <input type="text" name="message" placeholder="Type your message..." required>
            <button type="submit">Send</button>
        </form>
    </div>

    <script>
        // Auto-scroll to the latest message
        const chatbox = document.getElementById('chatbox');
        chatbox.scrollTop = chatbox.scrollHeight;
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat" not in session:
        session["chat"] = []

    chat = session["chat"]

    if request.method == "POST":
        # Handle resume upload
        if "resume" in request.files and request.files["resume"].filename != "":
            resume = request.files["resume"]
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(filepath)

            chat.append(("bot", f"👋 Hi! I’ve received your resume <b>{filename}</b>. Do you want me to summarize your skills or highlight your projects?"))

        # Handle user message
        elif "message" in request.form:
            user_msg = request.form["message"].strip()

            # Exit option
            if user_msg.lower() in ["exit", "quit"]:
                chat = []  # Clear the chat completely
                chat.append(("bot", "👋 Thank you for using the Resume Chatbot. Your session has ended."))
                session["chat"] = chat

            else:
                chat.append(("user", user_msg))
                bot_msg = chatbot_response(user_msg)
                chat.append(("bot", bot_msg))
                session["chat"] = chat

    return render_template_string(html_template, chat=chat)

if __name__ == "__main__":
    app.run(debug=True)

