from main import UserInput
from dotenv import load_dotenv
import os

load_dotenv()

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

user = UserInput()
