# DSBot

DSBot is a system designed for dataset QA. The user uploads a tabular dataset (e.g., a CSV file) and express a natural language question/statement (e.g., "Show me clusters in my data"). 

DSBot elaborates the question to produce and execute a data science analysis to provide an answer to the user's question.

## Description

## Installation
In order to correctly install and run the DSBot, please start by downloading the latest source from this GitHub repository:
> git clone https://github.com/DEIB-GECO/DSBot.git

Then _cd_ into the newly created _DSBot_ folder. By convenience we suggest to create a virtual environment. For example using conda:
> conda create -n dsbot python=3.7
>
> conda activate dsbot
>
> pip install -r requirements.txt

## Train / Import the model

## How to run
> cd DSBot
> 
> python app.py 

# In another window
> cd frontend

Only the first time install npm:
> npm install 

Run in development mode:
> npm run dev

Go to localhost:3000 to run the application
