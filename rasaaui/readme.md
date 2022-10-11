## RASA Bot made by the AUI guys

RASA bot that manages the conversation inside _Step 2 - Explain your analysis_ section of the webapp.

To communicate with the bot from a command line open a terminal, go to DSBot folder and use:
```
docker run -it -v ${pwd}/rasaaui:/app rasa/rasa:2.8.14-full shell
```
If you're using macOS or Linux please change ```${pwd}``` to ```$(pwd)```