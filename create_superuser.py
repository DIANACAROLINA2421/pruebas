from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("dianaa", "dianaa@gmail.com", "dianaa")
    print("Superusuario creado")
else:
    print("El superusuario ya existe")
