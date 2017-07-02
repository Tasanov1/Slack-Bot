import os
import time
from slackclient import SlackClient
import stackexchange

# methpdbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

so = stackexchange.Site(stackexchange.StackOverflow, app_key=None, impose_throttling=True)


slack = slack_client


def handle_command(command, channel):
    EXAMPLE_COMMAND = "help"
    response = "false"
    if command.startswith(EXAMPLE_COMMAND):
        response = "if you want ask something, use *"+"ask"+"* command\nif you want being tested, use *"+"quiz"+"* command\nif you want to get useful links,use *"+"links"+"* command"

    elif command.startswith("hello"):
	    response = "Hello!"

    elif command.encode('utf8')=='links ruby':
        response = "https://www.codeschool.com/learn/ruby\n https://www.codecademy.com/learn/ruby\n https://www.learnrubyonline.org/"

    elif command.encode('utf8')=='links java':
        response = "https://www.codecademy.com/learn/learn-java\n http://www.learnjavaonline.org/"

    elif command.encode('utf8')=='links python':
        response = "https://www.codecademy.com/learn/python\n https://www.codeavengers.com/profile#python\n https://www.codeschool.com/learn/python\n https://www.learn-php.org/"

    elif command.encode('utf8')=='links ruby on rails':
        response = "https://www.codecademy.com/learn/learn-rails"

    elif command.encode('utf8')=='links html & css':
        response = "https://www.codecademy.com/learn/web\n https://www.codeavengers.com/profile#html-css\n https://www.codeschool.com/learn/html-css"

    elif command.encode('utf8')=='links javascript':
        response = "https://www.codecademy.com/learn/javascript\n https://www.codeavengers.com/profile#javascript\n https://www.codeschool.com/learn/javascript"
    elif command.encode('utf8')=='links php':
        response = "https://www.codecademy.com/learn/php\n https://www.codeschool.com/learn/php\n https://www.learn-php.org/"
    elif command.encode('utf8')=='links sql':
        response = "https://www.codecademy.com/learn/learn-sql"
    elif command.startswith("links"):
        response = "Choose one from these:\n *"+"links Ruby"+"*\n*"+"links Java"+"*\n*"+"links Python"+"*\n*"+"links Ruby on rails"+"*\n*"+"links HTML & CSS"+"*\n*"+"links JavaScript"+"*\n*"+"links PHP"+"*\n*"+"links SQL"+"*"



    elif command.encode('utf8')=='java':
        response = "If A=10, then after B=++A, the value of B is _______."
    elif command.encode('utf8')=="11":
        response = "true"

    elif command.encode('utf8')=='python':
        response = "Which of the following data types is not supported in python?"
    elif command.encode('utf8')=="slice":
        response = "true"

    elif command.encode('utf8')=='ruby':
        response = "What is the output of this code?\n puts '7'*2"
    elif command.encode('utf8')=="77":
        response = "true"

    elif command.encode('utf8')=='ruby on rails':
        response = "CSRF stands for _____________"
    elif command.encode('utf8')=="cross-site request forgery":
        response = "true"

    elif command.encode('utf8')=='html & css':
        response = "Where in an HTML document is the correct place to refer to an external style sheet?"
    elif command.encode('utf8')=="<head>":
        response = "true"

    elif command.encode('utf8')=='javascript':
        response = "Is JavaScript a case-sensitive language?"
    elif command.encode('utf8')=="yes":
        response = "true"

    elif command.encode('utf8')=='php':
        response = "How to find the length of a string?"
    elif command.encode('utf8')=="strlen()":
        response = "true"

    elif command.encode('utf8')=='sql':
        response = "_____ is an open source SQL database"
    elif command.encode('utf8')=="mysql":
        response = "true"

    elif command.startswith("quiz"):
        response = "Choose one from these:\n *"+"Ruby"+"*\n*"+"Java"+"*\n*"+"Python"+"*\n*"+"Ruby on rails"+"*\n*"+"HTML & CSS"+"*\n*"+"JavaScript"+"*\n*"+"PHP"+"*\n*"+"SQL"+"*"


    elif command.startswith('ask'):
        soz = command.encode('utf8')[4:]
        print soz
        qs = so.search(intitle=soz)
        response=""
        count=0
        for i in qs:
            response+="https://stackoverflow.com/questions/"+str(i.id)
            response+="\n"
            if count==6:
                break
            count+=1

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response)



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("MethodBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
