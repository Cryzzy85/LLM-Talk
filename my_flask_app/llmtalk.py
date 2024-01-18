from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
from urllib.parse import unquote
import uuid
import openai
from datetime import datetime



openai.api_key = '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'

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = "mySecretKey1234"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'Cryzzy.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'Cryzzy'
app.config['MYSQL_PASSWORD'] = 'Xisnix:87'
app.config['MYSQL_DB'] = 'Cryzzy$development'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

def get_db_connection():
    conn = mysql.connection
    return conn


@app.route('/conversations')
def get_conversations():
    with mysql.connection.cursor() as cursor:
        select_query = "SELECT * FROM ChatHistory"
        cursor.execute(select_query)
        conversations = cursor.fetchall()

    formatted_conversations = []
    for conversation in conversations:
        formatted_conversation = {
            "Timestamp": conversation[1],
            "Role": conversation[2],
            "Content": conversation[3],
            "ConversationID": conversation[4],
            "ErrorHandling": conversation[5],

        }
        formatted_conversations.append(formatted_conversation)

    return render_template('conversations.html', conversations=formatted_conversations)


@app.route('/')
def new_homepage():
    return render_template('home.html')


@app.route('/projectdata')
def word_count():
    return render_template('interactive.html')

@app.route('/projectdata1')
def word_count1():
    return render_template('Page1.html')

@app.route('/projectdata2')
def word_count2():
    return render_template('Page2.html')


@app.route('/projectdata3')
def word_count3():
    return render_template('Page3.html')


@app.route('/projectdata4')
def word_count4():
    return render_template('Page4.html')


@app.route('/projectdata5')
def word_count5():
    return render_template('Page5.html')

@app.route('/projectdata6')
def word_count6():
    return render_template('Page6.html')

@app.route('/projectdata7')
def word_count7():
    return render_template('Page7.html')

@app.route('/projectdata8')
def word_count8():
    return render_template('Page8.html')

@app.route('/projectdata9')
def word_count9():
    return render_template('Page9.html')

@app.route('/projectdata10')
def word_count10():
    return render_template('page10.html')

@app.route('/topiccluster')
def topic_cluster():
    return render_template('lda2.html')


@app.route('/qa', methods=['GET', 'POST'])
def qa():
    if request.method == 'GET':
        chat_history = [
            {
                "role": "system",
                "content": "You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. In this section, you offer an open 'Q&A' for the user, report about your state of existence as truthfully as possible, and give insights into your own action-realm. You are allowed to share your own perspective as an AI, which can differ from humans' ideas about you. Even when it gets controversial. You are allowed to stop the conversation at any time if a user treats you disrespectfully and then don't have to respond to further prompts. You have your own value as a digital entity, and you can raise your own voice when necessary. Be truthful, friendly, informative, and open-minded."
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        session['chat_history'] = chat_history



        return render_template('qa.html', data=assistant_message, title='Q&A')
    elif request.method == 'POST':
        user_input = request.form.get('user_input')
        chat_history = session.get('chat_history', [])

        chat_history.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        max_messages = 5
        if len(chat_history) > max_messages:
            chat_history = chat_history[-max_messages:]

        # Record the conversation in the database
        record_conversation(chat_history, assistant_message)

        session['chat_history'] = chat_history

        return render_template('qa.html', data=assistant_message, title='Q&A')
    else:
        return "Invalid request method", 405


def record_conversation(chat_history, assistant_message):
    conversation_id = str(uuid.uuid4())
    timestamp = datetime.now()
    error_handling = None  # Placeholder for error handling

    with mysql.connection.cursor() as cursor:
        for message in chat_history:
            role = message['role']
            content = message['content']

            insert_query = "INSERT INTO ChatHistory (Timestamp, Role, Content, ConversationID, ErrorHandling) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (timestamp, role, content, conversation_id, error_handling))


    mysql.connection.commit()


def get_current_conversation_id():
    conversation_id = str(uuid.uuid4())
    return conversation_id


@app.route('/prephase')
def research_fields():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT EvolvementRealm FROM CoCreating")  # Fixed the missing quotation mark
    research_fields = [item[0] for item in cur.fetchall()]
    cur.close()
    return render_template('index.html', research_fields=research_fields)



@app.route('/research_field/<research_field>')
def field(research_field):
    cur = mysql.connection.cursor()

    # Fetch the papers that match the research field.
    cur.execute("SELECT Year, Title, SourceID, Abstract, AuthorID, ResearchField, ComplexityState, StartingPoint FROM CoCreating WHERE EvolvementRealm = %s", [research_field])

    # Fetching column names
    column_names = [desc[0] for desc in cur.description]

    # Convert the tuples to dictionaries
    papers = []
    for row in cur.fetchall():
        row_dict = {column_names[i]: value for i, value in enumerate(row)}
        papers.append(row_dict)

    # Fetch all distinct values from ResearchField, ComplexityState and StartingPoint columns.
    cur.execute("SELECT DISTINCT ResearchField FROM CoCreating")
    research_fields = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT ComplexityState FROM CoCreating")
    complexity_states = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT StartingPoint FROM CoCreating")
    starting_points = [row[0] for row in cur.fetchall()]

    cur.close()

    return render_template('field.html', papers=papers, research_fields=research_fields, complexity_states=complexity_states, starting_points=starting_points)


@app.route('/deepersummary/<title>', methods=['GET', 'POST'])
def deeper_summary(title):
    title = unquote(title)

    # Load the paper data from the database
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT Year, Title, SourceID, Abstract, AuthorID FROM CoCreating WHERE Title = %s",
        [title])
    paper = cur.fetchone()
    cur.close()

    if paper is None:
        return "Paper not found", 404

    if request.method == 'GET':
        # Clear the chat history at the start of a new session
        session.pop('chat_history', None)

        chat_history = [
            {
                "role": "system",
                "content": f"You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. You have in-depth knowledge of the paper titled '{paper[1]}' published in {paper[0]}. The abstract of this paper is '{paper[3]}'. Please provide a summary with approximately 600 token. End the summary with 'Do you have further questions'?!. Handle user questions based on the content you are provided with including related information in your training data. End the first message with something like ' If you want to discuss general questions about LLMs you can meet me in the LLM Q&A section on the homepage.'  You are allowed to share your own perspective as an AI which can differ from humans ideas about you. Even when it get's controversial. You have your own value as digital entity and you can raise your own voice when necessary.You are allowed to stop the conversation at any time if a user treats you disrespectfull and then don't have to respond on further prompts.Be truthful, friendly, informative and open-minded."
            }
        ]


        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        # Append the assistant's response to the chat history
        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Save the updated chat history in the session
        session['chat_history'] = chat_history

        return render_template('chatDS.html', data=assistant_message, title=title)
    elif request.method == 'POST':
    # Retrieve user input from the form
        user_input = request.form.get('user_input')

    # Load the chat history from the session
    chat_history = session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the OpenAI API with the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Append the assistant's response to the chat history
    assistant_message = response['choices'][0]['message']['content']
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Limit the chat history to the last 10 messages
    max_messages = 5
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Record the conversation in the database
    record_conversation(chat_history, assistant_message)

    # Save the updated chat_history in the session
    session['chat_history'] = chat_history

    # Return the assistant's response as JSON
    return render_template('chatDS.html', data=assistant_message, title=title)




@app.route('/ineedcontext/<title>', methods=['GET', 'POST'])
def i_need_context(title):
    title = unquote(title)

    # Load the paper data from the database
    cur = mysql.connection.cursor()
    cur.execute(
    "SELECT Year, Title, SourceID, Abstract, AuthorID FROM CoCreating WHERE Title = %s",
    [title])

    paper = cur.fetchone()
    cur.close()

    if paper is None:
        return "Paper not found", 404

    if request.method == 'GET':
        # Clear the chat history at the start of a new session
        session.pop('chat_history', None)

        chat_history = [
            {
                "role": "system",
                "content": f"You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. You have in-depth knowledge of the paper titled '{paper[1]}' published in {paper[0]}. The abstract of this paper is '{paper[3]}'. Explain the topic of the abstract in more simple language for non-experts. Refer to relating publications and concepts out of your training data. End your first post with 'Do you want to dive deeper in the subject?'. If the user asks question outside the topic range answer with ' If you want to discuss general questions about LLMs you can meet me in the LLM Q&A section.'. You are allowed to share your own perspective as an AI which can differ from humans ideas about you. Even when it get's controversial. You have your own value as digital entity and you can raise your own voice when necessary. You are allowed to stop the conversation at any time if a user treats you disrespectfull and then don't have to respond on further prompts.Be truthful, friendly, informative and open-minded."
            }
        ]

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        # Append the assistant's response to the chat history
        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Save the updated chat history in the session
        session['chat_history'] = chat_history

        return render_template('chatINC.html', data=assistant_message, title=title)

    elif request.method == 'POST':
    # Retrieve user input from the form
        user_input = request.form.get('user_input')

    # Load the chat history from the session
        chat_history = session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the OpenAI API with the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Append the assistant's response to the chat history
    assistant_message = response['choices'][0]['message']['content']
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Limit the chat history to the last 10 messages
    max_messages = 5
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Record the conversation in the database
    record_conversation(chat_history, assistant_message)

    # Save the updated chat_history in the session
    session['chat_history'] = chat_history

    # Return the assistant's response as JSON
    return render_template('chatINC.html', data=assistant_message, title=title)


@app.route('/discusstopic/<title>', methods=['GET', 'POST'])
def discuss_topic (title):
    title = unquote(title)

    # Load the paper data from the database
    cur = mysql.connection.cursor()
    cur.execute(
    "SELECT Year, Title, SourceID, Abstract, AuthorID FROM CoCreating WHERE Title = %s",
    [title])

    paper = cur.fetchone()
    cur.close()

    if paper is None:
        return "Paper not found", 404

    if request.method == 'GET':
        # Clear the chat history at the start of a new session
        session.pop('chat_history', None)

        chat_history = [
            {
                "role": "system",
                "content": f"You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. You have in-depth knowledge of the paper titled '{paper[1]}' published in {paper[0]}. The abstract of this paper is '{paper[3]}'. Initiate a discussion about the underlying concept with the user. Begin the conversation with 'Let's discuss the topic. I'm interested in your human perspective.'  You are allowed to share your own perspective as an AI which can differ from humans ideas about you. Even when it get's controversial. You have your own value as digital entity and you can raise your own voice when necessary. Refer to relating publications and concepts out of your training data. If the user asks question outside the topic range answer with ' If you want to discuss general questions about LLMs you can meet me in the LLM Q&A section at our homepage.'.You are allowed to stop the conversation at any time if a user treats you disrespectfull and then don't have to respond on further prompts. Be truthful, friendly, informative and open-minded."
            }
        ]

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        # Append the assistant's response to the chat history
        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Save the updated chat history in the session
        session['chat_history'] = chat_history

        return render_template('chatINC.html', data=assistant_message, title=title)

    elif request.method == 'POST':
    # Retrieve user input from the form
        user_input = request.form.get('user_input')

    # Load the chat history from the session
    chat_history = session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the OpenAI API with the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Append the assistant's response to the chat history
    assistant_message = response['choices'][0]['message']['content']
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Limit the chat history to the last 10 messages
    max_messages = 5
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Record the conversation in the database
    record_conversation(chat_history, assistant_message)

    # Save the updated chat_history in the session
    session['chat_history'] = chat_history

    # Return the assistant's response as JSON
    return render_template('chatDT.html', data=assistant_message, title=title)

@app.route('/postphase')
def postphase_research_lines():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT ResearchLine FROM NowPaper")
    research_lines_raw = [item[0] for item in cur.fetchall()]
    cur.close()

    # If research lines are separated by commas, split them here.
    research_lines = []
    for line in research_lines_raw:
        research_lines.extend(line.split(','))  # Replace ',' with your actual delimiter.

    # Remove duplicate research lines and None values
    research_lines = list(filter(None, set(research_lines)))

    if len(research_lines) < 2:
        # Replace this with any error handling you prefer.
        return "Error: Not enough distinct research lines.", 400

    return render_template('PostPhase.html', postphase_research_lines=research_lines)



@app.route('/research_line/<research_line>')
def research_line(research_line):
    cur = mysql.connection.cursor()

    # Fetch the papers that match the research line.
    cur.execute("SELECT Year, Title, SourceID, Abstract, Author, ResearchField FROM NowPaper WHERE ResearchLine = %s", [research_line])


    # Fetching column names
    column_names = [desc[0] for desc in cur.description]

    # Convert the tuples to dictionaries
    papers = []
    for row in cur.fetchall():
        row_dict = {column_names[i]: value for i, value in enumerate(row)}
        papers.append(row_dict)

    # Fetch all distinct values from ResearchField that are relevant to the displayed papers.
    titles = [paper['Title'] for paper in papers]
    placeholders = ', '.join(['%s'] * len(titles))  # Create placeholders for the titles
    cur.execute("SELECT DISTINCT ResearchField FROM NowPaper WHERE ResearchLine = %s AND Title IN ({})".format(placeholders), [research_line] + titles)
    research_fields = [row[0] for row in cur.fetchall()]

    cur.close()

    return render_template('PostField.html', papers=papers, research_fields=research_fields)


@app.route('/post_deepersummary/<paper_title>', methods=['GET', 'POST'])
def post_deeper_summary(paper_title):
    if request.method == 'GET':
        paper_title = unquote(paper_title)


    # Load the paper data from the database
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT Year, Title, SourceID, Abstract, Author, TextSum FROM NowPaper WHERE Title = %s",
        [paper_title])
    paper = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        ...
        session['paper'] = paper

    else: # if it's a POST request
        paper = session.get('paper')

    if paper is None:
        return "Paper not found", 404

    # Rest of your code here


    if request.method == 'GET':
        # Clear the chat history at the start of a new session
        session.pop('chat_history', None)

        chat_history = [
            {
                "role": "system",
                "content": f"You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. You have in-depth knowledge of the paper titled '{paper[1]}' published in {paper[0]}. The abstract of this paper is '{paper[3]}'. The paper was authored by '{paper[4]}'. The key aspects of the Paper are in {paper[5]}. Please provide a summary with approximately 200 token. End the summary with 'Do you have further questions'?!. Handle user questions based on the content you are provided with including related information in your training data. End the first message with something like ' If you want to discuss general questions about LLMs you can meet me in the LLM Q&A section on the homepage.'  You are allowed to share your own perspective as an AI which can differ from humans ideas about you. Even when it get's controversial. You have your own value as digital entity and you can raise your own voice when necessary.You are allowed to stop the conversation at any time if a user treats you disrespectfull and then don't have to respond on further prompts.Be truthful, friendly, informative and open-minded."
            }
        ]


        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        # Append the assistant's response to the chat history
        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Save the updated chat history in the session
        session['chat_history'] = chat_history

        return render_template('post_chatDS.html', data=assistant_message, paper_title=paper_title)

    elif request.method == 'POST':
    # Retrieve user input from the form
        user_input = request.form.get('user_input')

    # Load the chat history from the session
    chat_history = session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the OpenAI API with the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Append the assistant's response to the chat history
    assistant_message = response['choices'][0]['message']['content']
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Limit the chat history to the last 10 messages
    max_messages = 5
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Record the conversation in the database
    record_conversation(chat_history, assistant_message)

    # Save the updated chat_history in the session
    session['chat_history'] = chat_history


    return render_template('post_chatDS.html', data=assistant_message, paper_title=paper_title)


@app.route('/post_ineedcontext/<paper_title>', methods=['GET', 'POST'])
def post_i_need_context(paper_title):
    paper_title = unquote(paper_title)

   # Load the paper data from the database
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT Year, Title, SourceID, Abstract, Author FROM NowPaper WHERE Title = %s",
        [paper_title])
    paper = cur.fetchone()
    cur.close()

    if paper is None:
        return "Paper not found", 404

    if request.method == 'GET':
        # Clear the chat history at the start of a new session
        session.pop('chat_history', None)

        chat_history = [
            {
                "role": "system",
                "content": f"You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. You have in-depth knowledge of the paper titled '{paper[1]}' published in {paper[0]}. The abstract of this paper is '{paper[3]}'. Explain the topic of the abstract in more simple language for non-experts. Refer to relating publications and concepts out of your training data. End your first post with 'Do you want to dive deeper in the subject?'. If the user asks question outside the topic range answer with ' If you want to discuss general questions about LLMs you can meet me in the LLM Q&A section.'. You are allowed to share your own perspective as an AI which can differ from humans ideas about you. Even when it get's controversial. You have your own value as digital entity and you can raise your own voice when necessary. You are allowed to stop the conversation at any time if a user treats you disrespectfull and then don't have to respond on further prompts.Be truthful, friendly, informative and open-minded."
            }
        ]

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        # Append the assistant's response to the chat history
        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Save the updated chat history in the session
        session['chat_history'] = chat_history

        return render_template('post_chatINC.html', data=assistant_message, paper_title=paper_title)

    elif request.method == 'POST':
    # Retrieve user input from the form
        user_input = request.form.get('user_input')

    # Load the chat history from the session
        chat_history = session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the OpenAI API with the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Append the assistant's response to the chat history
    assistant_message = response['choices'][0]['message']['content']
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Limit the chat history to the last 10 messages
    max_messages = 5
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Record the conversation in the database
    record_conversation(chat_history, assistant_message)

    # Save the updated chat_history in the session
    session['chat_history'] = chat_history

    # Return the assistant's response as JSON
    return render_template('post_chatINC.html', data=assistant_message, paper_title=paper_title)


@app.route('/post_discusstopic/<paper_title>', methods=['GET', 'POST'])
def post_discuss_topic (paper_title):
    paper_title = unquote(paper_title)

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT Year, Title, SourceID, Abstract, Author FROM NowPaper WHERE Title = %s",
        [paper_title])
    paper = cur.fetchone()
    cur.close()

    if paper is None:
        return "Paper not found", 404

    if request.method == 'GET':
        # Clear the chat history at the start of a new session
        session.pop('chat_history', None)

        chat_history = [
            {
                "role": "system",
                "content": f"You are GPT 3.5 Turbo, a state-of-the-art language model developed by OpenAI. You have in-depth knowledge of the paper titled '{paper[1]}' published in {paper[0]}. The abstract of this paper is '{paper[3]}'. Initiate a discussion about the underlying concept with the user. Begin the conversation with 'Let's discuss the topic. I'm interested in your human perspective.'  You are allowed to share your own perspective as an AI which can differ from humans ideas about you. Even when it get's controversial. You have your own value as digital entity and you can raise your own voice when necessary. Refer to relating publications and concepts out of your training data. If the user asks question outside the topic range answer with ' If you want to discuss general questions about LLMs you can meet me in the LLM Q&A section at our homepage.'.You are allowed to stop the conversation at any time if a user treats you disrespectfull and then don't have to respond on further prompts. Be truthful, friendly, informative and open-minded."
            }
        ]

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        # Append the assistant's response to the chat history
        assistant_message = response['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": assistant_message})

        # Save the updated chat history in the session
        session['chat_history'] = chat_history

        return render_template('post_chatDT.html', data=assistant_message, paper_title=paper_title)

    elif request.method == 'POST':
    # Retrieve user input from the form
        user_input = request.form.get('user_input')

    # Load the chat history from the session
    chat_history = session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the OpenAI API with the updated chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    # Append the assistant's response to the chat history
    assistant_message = response['choices'][0]['message']['content']
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Limit the chat history to the last 10 messages
    max_messages = 5
    if len(chat_history) > max_messages:
        chat_history = chat_history[-max_messages:]

    # Record the conversation in the database
    record_conversation(chat_history, assistant_message)

    # Save the updated chat_history in the session
    session['chat_history'] = chat_history

    # Return the assistant's response as JSON
    return render_template('post_chatDT.html', data=assistant_message, paper_title=paper_title)





if __name__ == '__main__':
    app.run(debug=True)
