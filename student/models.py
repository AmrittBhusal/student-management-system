from django.db import models
from django.utils.text import slugify

# Create your models here.

class Parents(models.Model):
    father_name = models.CharField(max_length=100,null=True, blank=True)
    father_occupation = models.CharField( max_length=100, null=True, blank=True)
    father_mobile = models.CharField(max_length=50, blank=True, null=True)
    father_email = models.EmailField( blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)
    mother_mobile = models.CharField(max_length=50, blank=True, null=True)
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"
 
class Students(models.Model):
    #define the choices for gender
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Not specified', 'Not specified')    
    ]
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    student_id = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default='N', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    Student_class = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)
    admission_number = models.CharField(max_length=15, blank=True, null=True)
    section = models.CharField(max_length=15, blank=True, null=True)
    student_image = models.ImageField(upload_to='student_img/', blank=True, null=True)
    parent = models.OneToOneField(
        Parents, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="parent"
        )
    slug = models.SlugField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True,null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}--{self.last_name}--{self.student_id}")
        super(Students,self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.student_id}"