from flask import Flask, request, jsonify
# Import other necessary libraries and the 'agent' from your chatbot script

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat_response():
    data = request.json
    user_message = data['message']
    
    # Here, integrate with your chatbot to get a response
    # This assumes 'agent.run' is a function that takes the user's message and returns the chatbot's response.
    bot_response = agent.run(user_message)  # Replace 'agent.run' with your actual function call
    
    # Ensure you return a JSON object with a 'response' field
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Ensure this port matches the one in your JavaScript fetch call
