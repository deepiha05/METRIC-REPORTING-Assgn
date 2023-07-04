# Metric Reporting Application

![Metric Reporting](https://assets.toptal.io/images?url=https://bs-uploads.toptal.io/blackfish-uploads/components/blog_post_page/content/cover_image_file/cover_image/1272403/retina_500x200_0712-Bad_Practices_in_Database_Design_-_Are_You_Making_These_Mistakes_Dan_Newsletter-f90d29e5d2384eab9f4f76a0a18fa9a8.png)

## Overview

The Metric Reporting Application is an interactive web interface that provides insights into query processing metrics. It allows users to execute SQL queries and view important performance metrics, such as CPU usage, execution time, planning time, memory usage, and throughput.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- PostgreSQL database (configured with necessary permissions)
- Streamlit and other required Python packages


### Usage

    Update Database Configuration:
        Open the metrics.py file in a text editor.
        Locate the section that establishes a connection to the PostgreSQL database using psycopg2.connect.
        Update the database name, username, password, host, and port to match your database configuration.

    Run the Application:
        In the terminal, navigate to the project directory containing metrics.py.
        Run the Streamlit application using the following command in bash: streamlit run metrics.py

    Access the Application:
        Once the Streamlit app is running, it will display a URL in the terminal (e.g., http://localhost:8501).
        Open the URL in your web browser to access the Metric Reporting Application.

### How to Use

    Enter SQL Query:
        In the input box provided, type or paste your SQL query that you want to analyze.

    Analyze Query:
        Click the "Analyse" button to execute the query with performance analysis.
        The application will compute and display various query processing metrics.

    View Metrics:
        The application will show common metrics like query identifier, CPU usage, execution time, planning time, and memory usage.
        The plan table metrics will be displayed in an interactive grid, allowing you to explore the query plan details.