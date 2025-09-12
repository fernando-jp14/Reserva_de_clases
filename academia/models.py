from django.db import models

class ClassType(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "tipo_clase"
        verbose_name = "Tipo de Clase"
        verbose_name_plural = "Tipos de Clase"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Instructor(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    specialty = models.ForeignKey(
        ClassType,
        on_delete=models.SET_NULL,
        related_name="instructors",
        null=True,
        blank=True,
        help_text="Tipo de clase principal del instructor (opcional)."
    )
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "instructor"
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ClassSession(models.Model):
    title = models.CharField(max_length=128)
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.PROTECT,
        related_name="classes"
    )
    class_type = models.ForeignKey(
        ClassType,
        on_delete=models.PROTECT,
        related_name="classes"
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    capacity = models.PositiveIntegerField(null=False)
    # available_slots puede calcularse dinámicamente, pero dejamos un campo opcional
    available_slots = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Si desea guardar explícitamente. Si es NULL, se usa el valor calculado."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "class"
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["start"]

    def __str__(self):
        return f"{self.title} - {self.start.strftime('%Y-%m-%d %H:%M')}"

    def calculate_available_slots(self):
        """
        Método para usar desde la lógica de negocio:
        Si available_slots no está establecido, calcular como capacidad menos reservas activas.
        (La función para contar reservas activas se implementa en la aplicación bookings usando el modelo Booking.)
        """
        if self.available_slots is not None:
            return self.available_slots
        # Aquí devolvemos None por defecto: la aplicación bookings debe implementar el conteo real
        return None

