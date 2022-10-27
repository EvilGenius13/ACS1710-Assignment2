from email import message
from sqlite3 import OperationalError
from flask import Flask, request, render_template
import random

app = Flask(__name__)

def sort_letters(message):
    """A helper method to sort the characters of a string in alphabetical order
    and return the new string."""
    return ''.join(sorted(list(message)))


@app.route('/')
def homepage():
    """A homepage with handy links for your convenience."""
    return render_template('home.html')

@app.route('/froyo')
def choose_froyo():
    """Shows a form to collect the user's Fro-Yo order."""
    return render_template('froyo_form.html')
    """
    <form action="/froyo_results" method=GET">
        What is your favorite Fro-Yo flavor? <br/>
        <input type="text" name="flavor"><br/>
        What are you favorite Fro-Yo toppings?<br/>
        <input type="text" name="toppings"><br/>
        <input type="submit" value="Submit!">
    </form>
    """
    """The action= attribute specifies which URL the user will be sent to when they 
    submit the form. Here, the user will be sent to the URL /froyo_results/.
The method= attribute specifies the HTTP method the form will use to submit its results. 
It can be either GET or POST. At least one input field for the user to enter data. 
An input field with type="text" will accept a text input. 
Each input field must contain a name= attribute, which will be used to retrieve 
the data later. A submit button."""

@app.route('/froyo_results')
def show_froyo_results():
    # users_froyo_flavor = request.args.get('flavor')
    # users_froyo_toppings = request.args.get('toppings')
    # return f'You ordered {users_froyo_flavor} flavored Fro-Yo! with toppings {users_froyo_toppings}'
    context = {
        'froyo_flavor' : request.args.get('flavor'),
        'froyo_toppings' : request.args.get('toppings'),
    }
    return render_template('froyo_results.html', **context)
    """Here, we're using a dictionary called request.args, which stores 
    all of the data that the user entered into the form as key-value pairs. 
    We can retrieve each piece of user-entered data from the dictionary using .get()."""

@app.route('/favorites')
def favorites():
    return """
    <form action="/favorites_results" method="GET">
        What is our favorite color?<br/>
        <input type="text" name="color"><br/>
        What is your favorite animal?<br/>
        <input type="text" name="animal"><br/>
        What is your favorite city?<br/>
        <input type="text" name="city"><br/>
        <input type="submit" name"Submit!">
    </form>
    """

@app.route('/favorites_results')
def favorites_results():
    users_favorite_color = request.args.get('color')
    users_favorite_animal = request.args.get('animal')
    users_favorite_city = request.args.get('city')
    return f"Wow, I didn't know {users_favorite_color} {users_favorite_animal} lived in {users_favorite_city}!"


@app.route('/secret_message')
def secret_message():
    return """
    <form action="/message_results" method="POST">
    What message do you want to send?<br/>
    <input type="text" name="message"><br/>
    <input type="submit" name="Submit!">
    </form>
    """
    """Shows the user a form to collect a secret message. Sends the result via
    the POST method to keep it a secret!"""
    

@app.route('/message_results', methods=['POST'])
def message_results():
    secret_message = request.form.get('message')
    return sort_letters(secret_message)
    """Shows the user their message, with the letters in sorted order."""
    

@app.route('/calculator')
def calculator():
    """Shows the user a form to enter 2 numbers and an operation."""
    return render_template('calculator_form.html')
    """
    <form action="/calculator_results" method="GET">
        Please enter 2 numbers and select an operator.<br/><br/>
        <input type="number" name="operand1">
        <select name="operation">
            <option value="add">+</option>
            <option value="subtract">-</option>
            <option value="multiply">*</option>
            <option value="divide">/</option>
        </select>
        <input type="number" name="operand2">
        <input type="submit" value="Submit!">
    </form>
    """

@app.route('/calculator_results')
def calculator_results():
    users_first_num = int(request.args.get('operand1'))
    users_second_num = int(request.args.get('operand2'))
    users_option = request.args.get('operation')#given as add/subtract/multiply/divide
    
    if users_option == 'add':
        result = users_first_num + users_second_num
    elif users_option == 'subtract':
        result = users_first_num - users_second_num
    elif users_option == 'multiply':
        result = users_first_num * users_second_num
    elif users_option == 'divide':
        result = users_first_num / users_second_num
        

    context = {
        'operand1' : users_first_num,
        'operand2' : users_second_num,
        'operation' : users_option,
        'result' : result
    }
    
    
    
    return render_template('calculator_results.html', **context)
    # users_first_num = request.args.get('operand1')
    # users_second_num = request.args.get('operand2')
    # users_option = request.args.get('operation')#given as add/subtract/multiply/divide
    # users_first_num = int(users_first_num)
    # users_second_num = int(users_second_num)
    # if users_option == 'add':
    #     result = users_first_num + users_second_num
    #     return f'You chose to add {users_first_num} and {users_second_num}. Your result is: {result}'
    # elif users_option == 'subtract':
    #     result = users_first_num - users_second_num
    #     return f'You chose to subtract {users_first_num} and {users_second_num}. Your result is: {result}'
    # elif users_option == 'multiply':
    #     result = users_first_num * users_second_num
    #     return f'You chose to multiply {users_first_num} and {users_second_num}. Your result is: {result}'
    # elif users_option == 'divide':
    #     result = users_first_num / users_second_num
    #     return f'You chose to divide {users_first_num} and {users_second_num}. Your result is: {result}'


HOROSCOPE_PERSONALITIES = {
    'aries': 'Adventurous and energetic',
    'taurus': 'Patient and reliable',
    'gemini': 'Adaptable and versatile',
    'cancer': 'Emotional and loving',
    'leo': 'Generous and warmhearted',
    'virgo': 'Modest and shy',
    'libra': 'Easygoing and sociable',
    'scorpio': 'Determined and forceful',
    'sagittarius': 'Intellectual and philosophical',
    'capricorn': 'Practical and prudent',
    'aquarius': 'Friendly and humanitarian',
    'pisces': 'Imaginative and sensitive'
}

@app.route('/horoscope')
def horoscope_form():
    """Shows the user a form to fill out to select their horoscope."""
    return render_template('horoscope_form.html')

@app.route('/horoscope_results')
def horoscope_results():
    """Shows the user the result for their chosen horoscope."""

    # TODO: Get the sign the user entered in the form, based on their birthday
    name = request.args.get('users_name')
    horoscope_sign = request.args.get('horoscope_sign')
    #horoscope_sign = ''

    # TODO: Look up the user's personality in the HOROSCOPE_PERSONALITIES
    # dictionary based on what the user entered
    users_personality = ''
    for horoscope in HOROSCOPE_PERSONALITIES: 
        if horoscope == horoscope_sign: users_personality = HOROSCOPE_PERSONALITIES[horoscope]
    # TODO: Generate a random number from 1 to 99
    lucky_number = 0
    lucky_number = random.randint(1,99)
    context = {
        'horoscope_sign': horoscope_sign,
        'personality': users_personality, 
        'lucky_number': lucky_number,
        'users_name': name,
    }

    return render_template('horoscope_results.html', **context)

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
