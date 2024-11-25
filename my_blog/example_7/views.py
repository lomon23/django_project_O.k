from django.shortcuts import render

def main_page(request):
    return render(request, 'main.html', {
        'none_variable': None,
        'sample_dict': [
            {'name': 'Олександр', 'value': 25},
            {'name': 'Марія', 'value': 30},
            {'name': 'Іван', 'value': 20}
        ]
    })