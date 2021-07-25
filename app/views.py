from django.shortcuts import render
from app.tasks import add


x = add.delay(2, 3)
print(x.get(timeout=1))

