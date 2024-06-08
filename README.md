# TimeSheet Automation Project

## Project Description

This is a Python script that automates the process of downloading Timesheets for the previous week from a Toggl account. The script uses the Sync Playwright API to automate the process in a chromium browser.

## Installation

First, clone this repository:

```git clone https://github.com/user/your_project.git```

Then, you need to install playwright:

## Configuring the script

Before running the script, you need to set up your `secrets.yaml` file which should include the following:
```yaml
email: user@example.com # Replace with your actual email 
password: password # Replace with your actual password 
directory: Subdir/%s/Timesheets # This directory is a subdir of the users home dir the year is required for now
```

Ensure the `secrets.yaml` file is placed in the same directory as the Python script.

## Usage

After correctly setting up the `secrets.yaml` file, you can execute this script simply using Python:

```python main.py```

This script will automate the login process to Toggl, navigate to the reports section, and download the timesheet for the previous week as a PDF. The downloaded timesheet will be stored in the directory specified in the `secrets.yaml` file.

## License

[MIT](https://choosealicense.com/licenses/mit/)