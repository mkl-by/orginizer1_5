from django.shortcuts import render
import tasks


x = tasks.add.delay(2, 3)
print(x.get(timeout=1))

