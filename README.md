# Overview

I wrote this software to practice using Python, Pandas, and Matplotlib to analyze CSV data and answer questions with real data instead of guessing. The main dataset I used for my analysis was a video game sales dataset that includes game titles, platforms, genres, years, and regional and global sales values.

The main dataset used for the results in this report is stored in `data/vgsales.csv`.

Dataset source: [vgsales.csv](https://raw.githubusercontent.com/KNAI-AI/knai-workshop/main/data/vgsales.csv)

The purpose of this software is to:

- load a CSV dataset from the `data` folder
- let the user choose which dataset to analyze
- detect useful columns for analysis
- calculate average values by category
- find which groups appear the most in the top results
- save a graph to show part of the analysis visually

For my main analysis, the program answers these two questions using the `vgsales.csv` dataset:

1. Which genres have the highest average global sales?
2. Which platforms have the most top-selling games?

I also tested the program with other CSV files in the `data` folder to make sure it could work with more than one dataset.

[Software Demo Video](https://www.youtube.com/watch?v=GBkjDOIjLno)

# How to Run

1. Make sure Python 3 is installed.
2. Install the required libraries:

```bash
pip install pandas matplotlib
```

3. Run the program from the project folder:

```bash
python3 src/main.py
```

4. When the program starts, choose one of the CSV files shown from the `data` folder.

# Data Analysis Results

## Main dataset used for results

The main results below are based on `data/vgsales.csv`.

## Question 1: Which genres have the highest average global sales?

The program grouped the data by genre and calculated the average global sales for each genre. It then sorted the results from highest to lowest so I could see which genres performed best on average.

Answer:

- Platform: 0.94 million
- Shooter: 0.79 million
- Role-Playing: 0.62 million
- Racing: 0.59 million
- Sports: 0.57 million
- Fighting: 0.53 million
- Action: 0.53 million
- Misc: 0.47 million
- Simulation: 0.45 million
- Puzzle: 0.42 million
- Strategy: 0.26 million
- Adventure: 0.19 million

## Question 2: Which platforms have the most top-selling games?

The program defined top-selling games as the top 100 games by global sales. It then counted how many of those games appeared on each platform.

Answer:

- X360: 16 games
- Wii: 15 games
- DS: 13 games
- PS3: 9 games
- 3DS: 7 games
- GB: 6 games
- PS2: 6 games
- PS: 5 games
- PS4: 5 games
- SNES: 4 games
- N64: 4 games
- NES: 4 games
- GBA: 2 games
- 2600: 1 game
- PSP: 1 game
- PC: 1 game
- XB: 1 game

Extra details from the analysis:

- Rows used in analysis: 16,598
- Unique genres: 12
- Unique platforms: 31
- Year range in data: 1980 to 2020

The top 5 games used in the top-selling platform check were:

1. Wii Sports (Wii) - 82.74 million
2. Super Mario Bros. (NES) - 40.24 million
3. Mario Kart Wii (Wii) - 35.82 million
4. Wii Sports Resort (Wii) - 33.00 million
5. Pokemon Red/Pokemon Blue (GB) - 31.37 million

The program also saves a graph to:

`data/genre_average_global_sales.png`

# Testing

I tested the program with multiple CSV files in the `data` folder, including:

- `test_games.csv`
- `vgsales.csv`
- `steam.csv`

The `vgsales.csv` file was used for the main reported results in this README. The other files were used to test that the program could still load data, detect useful columns, print results, and save a graph.

# Development Environment

I used Visual Studio Code to write this project and GitHub to store the code.

This project was written in Python 3.

Libraries used:

- pandas
- matplotlib

# Useful Websites

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/users/index.html)
- [Python Documentation](https://docs.python.org/3/)
- [Kaggle](https://www.kaggle.com/)

# Future Work

- Add a third question for deeper analysis.
- Improve the graph formatting to make it easier to read.
- Let the user choose how many top rows to analyze instead of always using 100.
- Make the graph file name change based on the dataset being used.
