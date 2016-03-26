# Create the base class with a movie's properties
class Movie():
    def __init__(self, title, duration, genre, poster_image_url, trailer_youtube_url):
        self.title = title
        self.duration = duration
        self.genre = genre
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
