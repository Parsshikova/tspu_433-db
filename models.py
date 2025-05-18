from django.db import models

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название факультета")
    abbreviation = models.CharField(max_length=10, verbose_name="Аббревиатура", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    established_date = models.DateField(verbose_name="Дата основания", null=True, blank=True)

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"
        ordering = ['name']

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название группы")
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name="Факультет"
    )
    course = models.PositiveSmallIntegerField(verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ['course', 'name']
        unique_together = ['name', 'faculty']

    def __str__(self):
        return f"{self.name} ({self.faculty.abbreviation})"

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Пол"
    )
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    address = models.TextField(verbose_name="Адрес", blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students',
        verbose_name="Группа"
    )
    enrollment_date = models.DateField(verbose_name="Дата зачисления")
    is_active = models.BooleanField(default=True, verbose_name="Активный студент")
    photo = models.ImageField(
        upload_to='students/photos/',
        verbose_name="Фотография",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['group']),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    def get_current_course(self):
        if self.enrollment_date and self.group:
            # Логика расчета текущего курса на основе даты зачисления
            pass
        return None
