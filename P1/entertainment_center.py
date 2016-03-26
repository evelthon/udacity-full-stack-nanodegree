import media
import fresh_tomatoes

# Create a few instances to display in Fresh tomates
the_intern = media.Movie("The Intern",
                         "121",
                         "Comedy",
                         "http://cdn.traileraddict.com/content/warner-bros-pictures/intern2015.jpg", # noqa
                         "https://www.youtube.com/watch?v=ZU3Xban0Y6A")

the_internship = media.Movie("The Internship",
                             "119",
                             "Comedy",
                             "http://i.jeded.com/i/the-internship.24022.jpg",
                             "https://www.youtube.com/watch?v=cdnoqCViqUo")

the_100_foot_journey = media.Movie("The Hundred-Foot Journey",
                                   "122",
                                   "Comedy, "
                                   "Drama",
                                   "http://cdn.literarytraveler.com/wp-content/uploads/2015/02/HundredFootJourney1.jpg", # noqa
                                   "https://www.youtube.com/watch?v=h6H8pAKKkgQ") # noqa

# Generate the needed list of instances to feed to fresh_tomatoes
movies = [the_intern, the_internship, the_100_foot_journey]
fresh_tomatoes.create_movie_tiles_content(movies)
fresh_tomatoes.open_movies_page(movies)