# Rule-Based Chatbot

## Overview

This project is a simple rule-based chatbot that responds to user inputs using predefined rules. The chatbot identifies keywords or patterns in the user's message and provides appropriate responses using conditional statements (`if-else`) or pattern matching techniques.

The purpose of this project is to understand the fundamentals of:

* Natural Language Processing (NLP)
* Pattern matching
* Conditional logic
* Conversation flow
* Basic chatbot development

## Features

* Greets users with a welcome message.
* Responds to common greetings and questions.
* Uses predefined rules to generate responses.
* Handles unknown inputs with a default reply.
* Ends the conversation when the user types `bye`, `exit`, or `quit`.

## Technologies Used

* Python 3.x
* Standard Python libraries

## Project Structure

```text
Rule-Based-Chatbot/
│
├── app.py          # Main application file
├── chatbot.py      # Chatbot logic and response rules
├── README.md       # Project documentation
```

## Installation

1. Clone or download the project.
2. Ensure Python 3.x is installed.
3. Navigate to the project directory.

## How to Run

Run the following command:

```bash
python app.py
```

If your system uses `python3`, run:

```bash
python3 app.py
```

## How It Works

1. The application starts by displaying a welcome message.
2. The user enters a message.
3. The chatbot converts the input into lowercase for easier matching.
4. It checks the input against predefined rules using `if-else` statements or pattern matching.
5. If a match is found, an appropriate response is displayed.
6. If no match is found, the chatbot returns a default response.
7. The conversation continues until the user types `bye`, `exit`, or `quit`.

## Example Conversation

```text
Bot: Hello! I'm your chatbot. Type 'bye' to exit.

You: Hi
Bot: Hello! How can I help you?

You: What is your name?
Bot: I'm a simple rule-based chatbot.

You: Bye
Bot: Goodbye! Have a nice day.
```

## Learning Outcomes

* Understand rule-based chatbot design.
* Learn basic Natural Language Processing concepts.
* Practice using conditional statements and pattern matching.
* Build an interactive command-line application.

## Future Enhancements

* Add more response patterns.
* Use regular expressions for improved matching.
* Store conversation history.
* Develop a GUI using Tkinter or PyQt.
* Integrate machine learning or NLP libraries for smarter conversations.

## License

This project is intended for educational purposes and can be modified or extended as needed.
