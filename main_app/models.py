from django.db import models
from django.contrib.auth.models import User # update profile


# Category list 
CATEGORY_CHOICES = [
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Adventure', 'Adventure'),
    ('Family', 'Family'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Horror', 'Horror'),
]

# Type List 
TYPE_CHOICES = [
    ('TV', 'TV Show'),
    ('MV', 'Movie'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profiles/', default='profiles/default.jpg', blank=True)

    def __str__(self):  
        # This will display the profile in the admin panel as "Profile of username"
        return f"Profile of {self.user.username}"


class Show(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    season = models.IntegerField(default=1)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='TV') 
    image = models.ImageField(upload_to='shows/', default='shows/default.jpg')

# Title of the project 
    def __str__(self):
        return self.title 
    
    def average_rating(self):  
        ratings = self.ratings.all()
        if ratings:
            return round(sum(r.stars for r in ratings) / ratings.count(), 1)
        return 0

# Rating of the movie/series 
class Rating(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='ratings')
    user_name = models.CharField(max_length=100)
    stars = models.IntegerField()

    def __str__(self):
        return f"{self.user_name} rated {self.show} {self.stars} stars"
    
    class Meta:
        unique_together = ('show', 'user_name')  # only one rating by the user 
    
    

class Comment(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user_name} on {self.show}"