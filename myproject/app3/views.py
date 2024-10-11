
from django.shortcuts import render
import random

def guess_number(request):
    generated_number = None
    message = None
    if request.method == "POST":
        min_number = int(request.POST.get("min_number", 1))
        max_number = int(request.POST.get("max_number", 100))
        number_to_guess = random.randint(min_number, max_number)
        guess = int(request.POST.get("guess", 0))
        if guess < number_to_guess:
            message = "lower"
        elif guess > number_to_guess:
            message = "higher"
        else:
            message = "yeah"
            generated_number = number_to_guess

        return render(request, "guess_number.html", {
            "message": message,
            "generated_number": generated_number,
            "min_number": min_number,
            "max_number": max_number,
        })
    return render(request, "guess_number.html", {
        "min_number": 1,
        "max_number": 100,
    })
