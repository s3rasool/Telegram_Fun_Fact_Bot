# Telegram Fact Bot

Telegram Fact Bot is a simple Telegram bot that provides random useless facts to users upon request and allows users to receive periodic facts at a specified interval.

## Installation

1. Clone this repository:
   ```bash
   git clone this repostitory

Interact with the bot using the following commands:

/start: Start the bot and receive a greeting message.
/fact: Receive a random useless fact.
/facts <interval>: Start receiving periodic facts at the specified interval (in seconds). The interval must be greater than 5 seconds.
/unset: Stop receiving periodic facts.

## How it works

Upon receiving a command, the bot interacts with the Telegram API using the python-telegram-bot library.
The bot fetches random facts from the Useless Facts API using HTTP requests.
Users can opt-in to receive periodic facts by specifying an interval using the /facts command.
The bot manages periodic fact delivery using Telegram's JobQueue.

## Example

Start the bot by sending the /start command.
Receive a random fact by sending the /fact command.
Subscribe to periodic facts by sending the /facts <interval> command, e.g., /facts 60 to receive a fact every minute.
Stop receiving periodic facts by sending the /unset command.


## Contributions

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or create a pull request on GitHub.

