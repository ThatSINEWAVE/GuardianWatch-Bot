# GuardianWatch - Discord Member Scanner

Welcome to the Discord Member Scanner repository! This bot is your go-to tool for gathering and organizing information about Discord server members efficiently. Written entirely in Python and leveraging the power of Discord's Bot API along with the Google Sheets API, this bot offers versatility and ease of use across its three distinct modes: gsheets-mode, csv-mode, and combined-mode.

## Features

GSheets Mode: Automatically compiles a comprehensive list of user information at bot startup and sends it directly to your specified Google Sheets page.
CSV Mode: Utilizes the /inspect command to gather user information on-demand and outputs it as a CSV file directly in the chat.
Combined Mode: Merges the functionalities of GSheets and CSV modes, allowing the /inspect command to target either output format based on provided arguments (csv or gsheets).
Each mode operates as a separate Python file, giving you the flexibility to choose the version that best suits your needs.

## Information Collected

Currently, the bot collects the following information about each user:
- Username
- Discord ID
- Nickname
- Profile Picture URL
- Roles

## Future Enhancements

We're constantly looking to expand the bot's capabilities. Planned future updates include additional user details such as:
- Join Date
- Account Age
- Total Messages Sent
- Last Message Sent in the Server
- Getting Started

## To get the Discord Member Scanner up and running, follow these steps:

- Clone the Repository: Start by cloning this repository to your local machine.
- Install Dependencies: Ensure you have Python installed and the necessary packages.
- Setup Discord Bot: Follow Discord's official guide to set up a bot and obtain your token.
- Configure Google Sheets API: For GSheets mode, set up the Google Sheets API and obtain your credentials.
- Configuration: Populate the client_secret.json file with your Google Sheets credentials, and other necessary configurations.
- Run the Bot: Choose the mode you want to run and execute the corresponding Python file (gsheets-mode.py, csv-mode.py, or combined-mode.py).

## Usage

- GSheets Mode: Simply run the bot, and it will automatically populate your Google Sheet with member information at startup.
- CSV Mode: Use the /inspect command in your Discord server to trigger data collection and CSV file creation.
- Combined Mode: Use /inspect [csv/gsheets] to specify the output format for the data collection.

## Contribution
- Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to fork the repository, make your changes, and submit a pull request.

## License
- This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
- This bot is intended for educational and administrative purposes only. Ensure compliance with Discord's Terms of Service and obtain necessary permissions from server members before collecting data.
