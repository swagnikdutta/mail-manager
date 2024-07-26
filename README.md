# Mail Manager

A desktop app for managing emails in your Gmail account. It enables you to perform common operations on your emails such as marking them read/unread, moving them to spam/trash, etc.

## Prerequisites

- Follow steps 1-5 from the official [Google Workspace guide](https://developers.google.com/workspace/guides/get-started) to create your access credentials.
  - If you're using an OAuth client ID for authentication, exercise caution while choosing the scopes as they define the varying level of access this app will have to your mailbox.
  - For the purpose of reading emails and moving them around (spam/trash/etc), the following scopes are required:
    ```plaintext
    "https://www.googleapis.com/auth/gmail.labels",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly"
    ```
  - Once the credentials are created, download the `credentials.json` file.

## Installation

1. Clone the repository and navigate into it:
    ```sh
    git clone <repository_url>
    cd <repository_folder>
    ```
2. Place the `credentials.json` file at the root of the folder.
3. Create a virtual environment and activate it.
   ```
   python -m venv <env_name>
   source <env_name>/bin/activate
   ```
4. Install the requirements
   ```
   pip install -r requirements.txt
   ```

## Configuration

- Configure the `rules.json` file to define the criteria for selecting emails and the actions you intend to perform on them. Below is a sample configuration:

```json
[
  {
    "conditions": {
      "apply_predicate": "all",
      "condition_items": [
        {
          "field": "from",
          "predicate": "contains",
          "value": "newsletter@example.com"
        },
        {
          "field": "subject",
          "predicate": "contains",
          "value": "Weekly Update"
        }
      ]
    },
    "actions": [
      {
        "field": "mark_as_read",
      },
      {
        "field": "move_message",
        "predicate": "TRASH"
      }
    ]
  }
]
```

## Running the Program

1. Once the config is prepared, run the main program:
    ```sh
    python main.py
    ```
2. If you're running the program for the first time, you will be asked to allow the permissions the app requires.
3. Upon successful authorization, a `token.json` file will be created. If you need to update the scopes, delete the existing `token.json` file and run the program again.

## [Demo](https://drive.google.com/file/d/1Vq_1WVbW6SWdsn3COe2XTDmSa64mcclw/view?usp=sharing)


