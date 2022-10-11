# Conversational blocks

This directory contains a series of JSON files. </br>
These files are used by the **conversation manager** in order to help
the user make decisions once they have decided the type of analysis
they want to perform.

Each JSON file must have the following fields in order to be used by
the manager:
- `name`: string
- `description`: string
- `parameters`: array of _parameters_

Each _parameter_ must have the following fields:
- `is_special`: yes / no
- `question`: string
- `answer_type`: int / float / string
- `help`: string
- [**only if is_special is true**] `media_type`: text / img / GIF / video (??)
- [**only if is_special is true**] `media_path`: string

Example:
```
{
  "name": "<name_of_your_block>",
  "description": "<what your block does>",
  "parameters": [
    {
      "is_special": "yes",
      "question": "<question you want to ask to the user>",
      "answer_type": "string",
      "help": "<this message will be displayed if the user asks for help>",
      "media_path": "<your/resource/path>",
      "media_type": "img"
    }
  ]
}
```

