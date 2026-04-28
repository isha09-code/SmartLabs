from django.db import models
from django.utils import timezone


# 🧪 Equipment Model
class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('computer', 'Computer'),
        ('geography', 'Geography'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    available = models.IntegerField(blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='physics'
    )

    lab_blocked: bool = False
    free_time: str | None = None

    def __str__(self):
        return f"{self.name} ({self.category})"


# 📦 Booking Model (Student)
class Booking(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    # 👤 Student Info
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    roll = models.CharField(max_length=20)
    pin = models.CharField(max_length=10)

    quantity = models.IntegerField(default=1)

    # ⏰ Time Info (IN MINUTES)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration = models.IntegerField(default=60)

    purpose = models.TextField(blank=True, null=True)

    booked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} booked {self.equipment.name}"

    # 🔥 End Time (MINUTES)
    @property
    def end_time(self):
        from datetime import datetime, timedelta
        start = datetime.combine(self.booking_date, self.booking_time)
        end = start + timedelta(minutes=self.duration)
        return end.time()

    # 🔥 SMART DURATION DISPLAY
    @property
    def duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60

        if hours and minutes:
            return f"{hours} hour {minutes} min"
        elif hours:
            return f"{hours} hour"
        else:
            return f"{minutes} min"

    class Meta:
        ordering = ['-booking_date', '-booking_time']


# 🏫 Teacher Full Lab Booking
class LabBooking(models.Model):
    LAB_CHOICES = [
        ('physics', 'Physics Lab'),
        ('chemistry', 'Chemistry Lab'),
        ('biology', 'Biology Lab'),
        ('computer', 'Computer Lab'),
        ('geography', 'Geography Lab'),
    ]

    lab = models.CharField(max_length=50, choices=LAB_CHOICES)
    teacher_name = models.CharField(max_length=100)

    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(default=60)   # MINUTES

    def __str__(self):
        return f"{self.teacher_name} booked {self.lab}"

    # 🔥 End Time (MINUTES)
    @property
    def end_time(self):
        from datetime import datetime, timedelta
        start = datetime.combine(self.date, self.time)
        end = start + timedelta(minutes=self.duration)
        return end.time()

    # 🔥 SMART DISPLAY (OPTIONAL)
    @property
    def duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60

        if hours and minutes:
            return f"{hours} hour {minutes} min"
        elif hours:
            return f"{hours} hour"
        else:
            return f"{minutes} min"

    class Meta:
        ordering = ['-date', '-time']