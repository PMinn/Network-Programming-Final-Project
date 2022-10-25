#import sys
#sys.path.insert(1, './model')
import eel

# Set web files folder
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('main.html', size=(300, 200))  # Start
