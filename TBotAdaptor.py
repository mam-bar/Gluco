import telepot
from telepot.loop import MessageLoop
import time
from TelegramTools.existenceInquiry import TAuthentication
from TelegramTools.injection import Injection
from TelegramTools.pullObservation import pullObservations
from RegisteryTools.RegisterTelegram import registerService
from telepot.namedtuple import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


class Mybot:
    def __init__(self, client_id, token):
        self.client_id = client_id
        self.token = token
        self.bot = telepot.Bot(self.token)
        self.callback_dict = {
            "chat": self.on_chat_message,
            "callback_query": self.callback_queries,
        }
        self.user_state = {}
        registerService(self.client_id, self.token)

    def start(self):
        MessageLoop(self.bot, self.callback_dict).run_as_thread()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        ###             Authentication phase
        if chat_id not in self.user_state:
            # Initial state: Send a welcome message and ask for username
            self.user_state[chat_id] = {"state": "awaiting_username", "password": None}
            self.bot.sendMessage(chat_id, "Welcome to our health service!")
            time.sleep(0.5)
            self.bot.sendMessage(chat_id, "Enter your 'HealthInsul' username: ")

        elif (
            chat_id in self.user_state
            and self.user_state[chat_id]["state"] == "awaiting_username"
        ):
            # Save the username and ask for the password
            self.user_state[chat_id]["username"] = msg["text"]
            self.user_state[chat_id]["state"] = "awaiting_password"
            self.bot.sendMessage(chat_id, "Now enter your 'HealthInsul' password: ")
        elif (
            chat_id in self.user_state
            and self.user_state[chat_id]["state"] == "awaiting_password"
        ):
            username = self.user_state[chat_id]["username"]
            password = msg["text"]
            self.user_state[chat_id]["password"] = msg["text"]
            if TAuthentication().patient(username, password):
                self.user_state[chat_id]["state"] = "Authenticated"
                self.bot.sendMessage(chat_id, "Login Successful!")
                self.on_home(chat_id)
            else:
                self.bot.sendMessage(
                    chat_id, "Invalid username or password!\nHit /start to start over"
                )
                self.user_state.pop(chat_id)
        ###             Authentication Accomplished
        ###             Now, Talk to actuator

        elif self.is_auth(chat_id) and msg["text"] == "Yes, Inject!":
            user = self.user_state[chat_id]["username"]
            sensor = Injection().getSensor(user)
            injection_response = Injection().injectionCommand(user, sensor)
            self.bot.sendMessage(chat_id, injection_response)
            self.on_home(chat_id)

        elif self.is_auth(chat_id) and msg["text"] == "Cancel Injection":
            self.bot.sendMessage(chat_id, "Injection Aborted!")
            self.on_home(chat_id)

        ###             Retrieve results in monitoring section

        elif self.is_auth(chat_id) and msg["text"] == "Last 5 mins":
            user = self.user_state[chat_id]["username"]
            inquiry = pullObservations().getLastN(user, 5)
            self.bot.sendMessage(chat_id, self.parseInquiry(inquiry))
            self.on_home(chat_id)

        elif self.is_auth(chat_id) and msg["text"] == "Last 15 mins":
            user = self.user_state[chat_id]["username"]
            inquiry = pullObservations().getLastN(user, 15)
            self.bot.sendMessage(chat_id, self.parseInquiry(inquiry))
            self.on_home(chat_id)

        elif self.is_auth(chat_id) and msg["text"] == "Last 60 mins":
            user = self.user_state[chat_id]["username"]
            inquiry = pullObservations().getLastN(user, 60)
            self.bot.sendMessage(chat_id, self.parseInquiry(inquiry))
            self.on_home(chat_id)

        ###             Connecting client to healthcare provider

        elif (
            self.is_auth(chat_id)
            and msg["text"] == "Connect me to the healthcare provider"
        ):  # hardcoded for the now
            self.bot.sendMessage(
                chat_id, "Message your health provider here: @mohammadbaratiit"
            )
            self.on_home(chat_id)
        else:
            self.bot.sendMessage(chat_id, "Invalid command!\nTry again...")
            self.on_home(chat_id)

    ###                 Interactions after pressing home buttons

    def callback_queries(self, msg):
        query_id, chat_id, query = telepot.glance(msg, flavor="callback_query")

        if self.is_auth(chat_id) and query == "Monitor":
            self.on_monitor(chat_id)

        elif self.is_auth(chat_id) and query == "Inject":
            self.on_injection(chat_id)

        elif self.is_auth(chat_id) and query == "Help":
            self.on_help(chat_id)
        elif self.is_auth(chat_id) and query == "Logout":
            self.bot.sendMessage(
                chat_id, "Logout successful!\nHit /start to start over"
            )
            self.user_state.pop(chat_id)

    def is_auth(self, chat_id):
        if self.user_state[chat_id]["state"] == "Authenticated":
            return True
        else:
            return False

    ###                 The main inline buttons to appear after every interaction

    def on_home(self, chat_id):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Monitor", callback_data="Monitor"),
                    InlineKeyboardButton(text="Inject", callback_data="Inject"),
                    InlineKeyboardButton(text="Help", callback_data="Help"),
                    InlineKeyboardButton(text="Logout", callback_data="Logout"),
                ]
            ]
        )
        self.bot.sendMessage(
            chat_id, "What services can I offer you?", reply_markup=keyboard
        )

    ###                 Injection reply keyboard setup

    def on_injection(self, chat_id):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes, Inject!"),
                    KeyboardButton(text="Cancel Injection"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=False,
        )
        self.bot.sendMessage(
            chat_id, "Do you want to inject insulin now?", reply_markup=keyboard
        )

    ###                 Monitor reply keyboard setup

    def on_monitor(self, chat_id):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Last 5 mins"),
                    KeyboardButton(text="Last 15 mins"),
                    KeyboardButton(text="Last 60 mins"),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=False,
        )
        self.bot.sendMessage(
            chat_id, "Select a timeframe to be shown: ", reply_markup=keyboard
        )

    ###                 Help reply keyboard setup

    def on_help(self, chat_id):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Connect me to the healthcare provider")]],
            resize_keyboard=True,
            one_time_keyboard=True,
            is_persistent=False,
        )
        self.bot.sendMessage(
            chat_id,
            "Do you want to contact your healthcare provider?",
            reply_markup=keyboard,
        )

    def parseInquiry(self, inquiry):
        try:
            return f"Average:{inquiry['Average']}\nHighest: {inquiry['Highest']}\nLowest: {inquiry['Lowest']}"
        except:
            pass


if __name__ == "__main__":
    token = "7504596852:AAHD3ZDYjDcR4LFPXNrw-fiXOV4GSBSQffY"
    client_id = "MyTelePot"
    first_bot = Mybot(client_id, token)
    first_bot.start()
    while True:
        time.sleep(2)
