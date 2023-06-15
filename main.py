import pandas as pd
import logging

# Define Movie class


class Movie:
    """
    Initializes the Movie object with two CSV file paths; sets up the logger.
    """
    def __init__(self, csv_file1, csv_file2):
        self.csv_file1 = csv_file1
        self.csv_file2 = csv_file2
        self.data_frame1 = None
        self.data_frame2 = None
        self.combined_data_frame = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

# Step 1. Load the dataset from a CSV file using pandas.

    def load_dataset(self):
        """
        Loads the datasets from the provided CSV files into DataFrames.
        """
        try:
            self.data_frame1 = pd.read_csv(self.csv_file1, low_memory=False)
            self.data_frame2 = pd.read_csv(self.csv_file2, low_memory=False)
            self.logger.info("Datasets loaded successfully.")
        except FileNotFoundError:
            self.logger.error("Dataset file not found.")

# Step 2. Print the number of the unique movies in the dataset.

    def print_unique_movies(self):
        """
        Prints the number of unique movies in the dataset.
        """
        if self.data_frame1 is not None:
            unique_movies_count = len(self.data_frame1['title'].unique())
            print("Number of unique movies: ", unique_movies_count)
        else:
            self.logger.error("Movies dataset not loaded.")

# Step 3. Print the average rating of all the movies.

    def print_average_rating(self):
        """
        Prints the average rating of all the movies.
        """
        if self.data_frame2 is not None:
            average_rating = self.data_frame2['rating'].mean()
            print("Average rating of all movies: ", average_rating)
        else:
            self.logger.error("Ratings dataset not loaded.")

# Step 4. Print the top 5 highest rated movies.

    def print_top_rated_movies(self):
        """
        Sorts ratings dataset by rating in descending order and gets the top 5 rated movie IDs.
        Finds the movie titles from the metadata dataset using the matched movie IDs
        """
        if self.data_frame2 is not None:
            sorted_ratings = self.data_frame2.sort_values(by='rating', ascending=False)
            top_movie_ids = sorted_ratings.head(5)['movieId'].tolist()

            if self.data_frame1 is not None:
                top_movies = self.data_frame1[self.data_frame1['id'].isin(top_movie_ids)]
                print("Top 5 highest rated movies: ")
                for index, row in top_movies.iterrows():
                    print(f"{row['title']}: {row['rating']}")
            else:
                self.logger.error("Movies dataset not loaded.")
        else:
            self.logger.error("Ratings dataset not loaded.")

# Step 5. Print the number of movies released each year.

    def print_movies_per_year(self):
        """
        Prints the number of movies released each year.
        """
        if self.data_frame1 is not None:
            self.data_frame1['year'] = pd.to_datetime(self.data_frame1['release_date'], errors='coerce').dt.year
            movies_per_year = self.data_frame1['year'].value_counts().sort_index()
            print("Number of movies released each year: ")
            print(movies_per_year)
        else:
            self.logger.error("Movies dataset not loaded.")

# Step 6. Print the number of movies in each genre.

    def print_movies_per_genre(self):
        """
        Prints the number of movies in each genre.
        """
        if self.data_frame1 is not None:
            genres = self.data_frame1['genres'].str.split(',').explode().str.strip()
            movies_per_genre = genres.value_counts()
            print("Number of movies in each genre: ")
            print(movies_per_genre)
        else:
            self.logger.error("Movies dataset not loaded.")

# Step 7. Save the dataset to a JSON file.

    def merge_datasets(self):
        """
        Merges the two datasets based on movie IDs.
        """
        if self.data_frame1 is not None and self.data_frame2 is not None:
            self.data_frame2['movieId'] = self.data_frame2['movieId'].astype('str')
            self.combined_data_frame = pd.merge(
                self.data_frame1,
                self.data_frame2,
                left_on='id',
                right_on='movieId',
                how='inner'
            )
            self.logger.info("Datasets merged successfully.")
        else:
            self.logger.error("One or both datasets not loaded.")

    def save_to_json(self, json_file):
        """
        Saves the dataset to a JSON file.
        """
        if self.combined_data_frame is not None:
            self.combined_data_frame.to_json(json_file, orient="records")
            self.logger.info(f"Combined dataset saved to {json_file}.")
        else:
            self.logger.error("Combined dataset not available.")


movie = Movie("movies_metadata.csv", "ratings.csv")
movie.load_dataset()
movie.print_unique_movies()
movie.print_average_rating()
movie.print_top_rated_movies()
movie.print_movies_per_year()
movie.print_movies_per_genre()
movie.merge_datasets()
movie.save_to_json("combined_dataset.json")



