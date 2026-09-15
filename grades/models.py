from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from school.models import StudentProfile,SchoolClass,Subject,TeacherProfile

class Grade(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name='grades'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name='grades'
    )
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.PROTECT,
        related_name='grades'
    )
    term = models.CharField(
        max_length=50
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    notes = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'term'],
                name='unique_student_subject_term_grade'
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.subject} - "
            f"{self.term}"
        )
    
# Use CASCADE when the child object shouldn't exist without the parent.
# PROTECT Don't allow the parent to be deleted if related objects exist.
# SET_NULL set the foreign key to NULL instead of deleting the object.