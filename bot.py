import telebot
import requests
token = '645fc2036fcc076af765948e37fcf3087dd95b8d'
username = 'bdloser'

bot = telebot.TeleBot("6176575414:AAHx1qPlSNDbBlVeHEDgw5AsthFyAUQR8lQ")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Python code compiler bot! Send me your Python code to compile.")

@bot.message_handler(content_types=['text'])
def compile_code(message):
    if message.text.startswith("[py]") and message.text.endswith("[/py]"):
        # Extract the code between the [py] and [/py] tags
        code = message.text[4:-5]

        # Send the user's code to the PythonAnywhere API
        response = requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/run/python3/', 
                        headers={'Authorization': 'Token {token}'},
                        json={'python_version': '3.10', 'code': code})

        # If the request was successful, return the output of the compiled code
        if response.status_code == 201:
            output = response.json()['output']
            bot.reply_to(message, f"Output:\n{output}")
        else:
            bot.reply_to(message, "There was an error compiling your code. Please try again.")
    else:
        bot.reply_to(message, "Please send your Python code inside [py] and [/py] tags.")

bot.polling()
