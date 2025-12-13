# ⚾ MLB Restaurant Finder - DSCI 551 Final Project - Darren Parry

## Project Description
- This application is a NoSQL-like database system built from scratch using Python. It parses raw JSON data regarding MLB stadiums and nearby restaurants without using standard libraries like `json` or `pandas` for data processing. The Streamlit interface allows others to easily toggle
through stadiums sorting for how they want to see the data in different queries.

## Project Structure:
- 'main.py': Front-end Streamlit application code
- 'functions.py': Contains the database logic
- 'parser.py': Contains the parsing logic
- 'data/': Data direcotry contains JSON datasets for all MLB teams

## Required Software:

- streamlit, 'pip install streamlit'
- terminal
- dsci551_project zipped file

## Running Project:

- Make sure you have the zipped file, dsci551_project, downloaded, unzipped, and located
- Open your terminal and navigate to where your folder is
- e.g. if your folder is on your desktop from darrenparry@Darrens-MacBook-Air ~ %, cd Desktop, then cd dsci551_project
- Once you are in the correct directory, run  the following command: 'streamlit run main.py'
- Your browser should pop up with the streamlit app and there is instructions on the page for how to navigate through the app
- To interrupt the connection, go back to the terminal and press, ctrl + c
