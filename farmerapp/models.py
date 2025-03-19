from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)
    user_location = models.CharField(max_length=50,default='Unknown')
    user_profile = models.ImageField(upload_to='images/user')
    status = models.CharField(max_length=15,default='Pending')
    otp = models.CharField(max_length=6,default=0) 


    class Meta:
        db_table = 'User_details'


from django.db import models

# Model for storing image and related details
class CropPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the prediction to a user
    uploaded_image = models.ImageField(upload_to='images/crop_predictions/')  # Store the uploaded image
    plant_type = models.CharField(max_length=100)  # The type of the plant/tree predicted
    growth_tips = models.TextField()  # A string to store growth tips
    care_tips = models.TextField()  # A string to store care tips
    pesticide_suggestions = models.TextField()  # A string to store pesticide suggestions
    timestamp = models.DateTimeField(auto_now_add=True)  # Time when the prediction was made

    class Meta:
        db_table = 'crop_predictions'




class Conversation(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"User: {self.user_message[:50]}..."


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    rating = models.IntegerField()
    additional_comments = models.TextField()
    
    class Meta:
        db_table = 'Feedback_details'






















        

class FarmerQuery(models.Model):
    query_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact_number = models.CharField(max_length=50)
    query_type = models.CharField(max_length=20, choices=[('General', 'General Inquiry'), ('Technical', 'Technical Issue'), ('CropInfo', 'Crop Information')])
    crop_information = models.TextField()
    query_subject = models.CharField(max_length=20, choices=[('PestControl', 'Pest Control'), ('Fertilization', 'Fertilization'), ('Disease', 'Crop Disease'), ('Other', 'Other')])
    specific_issue = models.TextField()
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    weather_condition = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Farmer_Query'





class Appointment(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    appointment_date = models.DateField()
    query_subject = models.CharField(max_length=20, choices=[('PestControl', 'Pest Control'),
                                                             ('Fertilization', 'Fertilization'),
                                                             ('Disease', 'Crop Disease'),
                                                             ('Other', 'Other')])
    additional_info = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15,default='Pending')


    class Meta:
        db_table = 'Appointment_details'