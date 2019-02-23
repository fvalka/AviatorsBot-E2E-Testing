# End to End Testing for AviatorsBot

This is a test suite of automated end to end tests for [AviatorsBot](https://github.com/fvalka/AviatorsBot).

## Concept
The tests connect to the production instances of the Telegram servers and send the bots commands to the Bot configured
in config/config.py. 

Tests must be processed sequentially, for each sent command the test waits for the response until the configured timeout
is reached. In that case the test fails. 

## Usage / SetUp

The setup of the test suite requires a production system Telegram account!

1. Obtain an API ID and API Hash on my.telegram.org 
2. Set the environment variables TELEGRAM_API_ID and TELEGRAM_API_HASH
3. Run the test suite locally to login and generate the session which is stored in secrets/telegram.session
4. Deploy to Kubernetes or another platform for running the tests using the environment variables defined above and the
 session