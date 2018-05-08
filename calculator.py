from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    sum = 0
    for i in range(len(args)):
      sum += int(args[i])
    return str(sum).encode("utf-8")
# TODO: Add functions for handling more arithmetic operations.

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    diff = int(args[0])
    for i in range(1, len(args)):
      diff -= int(args[i])
    return str(diff).encode("utf-8")

def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    prod = 1
    for i in range(len(args)):
      prod *= int(args[i])
    return str(prod).encode("utf-8")

def divide(*args):
    """ Returns a STRING with the division of the arguments """

    div = int(args[0])
#    if div == 0:
#      not_found()
#      return status, body
    for i in range(1, len(args)):
      div /= int(args[i])
    return str(div).encode("utf-8")

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    dissect = path.split('/')
    dissect.pop(0)
    func = dissect.pop(0)
    args =  dissect
#    return func, args
    return args, func
    # we get here if no url matches
    raise NameError

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
#        elif path == '/':
#          status = "200 OK"
#          body = "<html>Here's how to use this page...</html>"
        args, func = resolve_path(path)
        """
        For some reason when I try to use 'body = func(*args)'
        I get AttributeError: 'str' object has no attribute 'decode'.
        In order to get this turned in on time, I used a series of 
        if/else statements to make the calculator function.
        """
#        body = func(*args)
        if func == 'add':
          body = add(*args)
          body = body.decode('utf-8')
        elif func == 'subtract':
          body = subtract(*args)
          body = body.decode('utf-8')
        elif func == 'multiply':
          body = multiply(*args)
          body = body.decode('utf-8')
        elif func == 'divide':
          body = divide(*args)
          body = body.decode('utf-8')
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
#        headers.append(('Content-length', '30'))
        start_response(status, headers)
#        body = func
#        body = body.decode('utf-8')
#        body = "The answer is: " + body + " " + func + str(args)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
