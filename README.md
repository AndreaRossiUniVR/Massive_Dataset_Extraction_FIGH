# Massive Dataset Extraction and Analysis of FIGH

This repository contains a project that aims to extract, clean, and analyze a massive dataset from the Italian Handball Federation (Federazione Italiana Giuoco Handball, FIGH). The dataset consists of numerous PDF files, each containing the details of a specific game. The project utilizes Python for data extraction, SQLite for data storage, and Jupyter Notebook for data analysis and visualization.

## Introduction

The goal of this project is to extract valuable insights from the dataset provided by the FIGH. By utilizing techniques for data extraction, cleaning, and analysis, we aim to uncover patterns, trends, and statistics related to Italian handball games. The project focuses on player performance, goal scoring, and team analysis.

## Data Extraction and Cleaning

The data extraction process involves downloading PDF files from the FIGH website and using the PyPDF2 library to read and parse the contents. Regular expressions are used to extract specific information, such as game numbers, dates, game categories, team names, player details, and scores. The extracted data is then stored in a structured format for further analysis.

## Database Setup and Data Insertion

An SQLite database is set up to store the extracted data. The database consists of three tables: Games, Teams, and Players. The data from the PDF files is inserted into these tables, ensuring that each row has a unique identifier. The database provides a structured and efficient way to store and query the extracted data.

## Data Analysis and Visualization

The project includes various data analysis and visualization techniques to gain insights from the dataset. Two key features are highlighted:

1. Player's Goals per Game and Average Change in Wins and Losses: This feature focuses on analyzing the performance of selected players in terms of goals per game. It also explores how this average changes in different game outcomes, such as wins and losses. The results are visualized using bar charts, providing a clear comparison of player performance.

2. Goals Distribution and Comparison with a Predictive Model: This feature examines the distribution of goals among all players in a selected category and team. It compares the actual distribution with a predictive model based on a 1/x distribution. The visualization includes a histogram overlaid with the predicted distribution, enabling a comparison of actual and expected goal distributions.

## Dataset Inconsistency

While the project has been successful in extracting and analyzing the dataset, it is important to note some inconsistencies and challenges encountered during the process. These include empty PDF files, typos in player details, and format inconsistencies in certain PDFs. These issues have been acknowledged, but their resolution is not within the scope of this project. Future developments should address these inconsistencies for more comprehensive and accurate analysis.

## Conclusions and Future Work

This project demonstrates the potential of data extraction, cleaning, and analysis in the context of Italian handball statistics. It provides valuable insights into player performance, goal scoring, and team analysis. However, there are opportunities for further analysis and development. Future work could include expanding the dataset to cover a longer time period, incorporating additional game details, and developing a frontend application for displaying advanced statistics.

In conclusion, this project showcases the power of data analysis in the field of sports statistics. By leveraging Python, SQLite, and Jupyter Notebook, we have successfully extracted, cleaned, and analyzed a massive dataset from the FIGH. The insights gained from this analysis can benefit teams, coaches, and players in their pursuit of improved performance and strategic decision-making.

