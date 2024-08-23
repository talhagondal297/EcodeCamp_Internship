# calculator/views.py
from django.shortcuts import render

def calculator_view(request):
    display = ""
    error = None
    session = request.session

    if request.method == "POST":
        button = request.POST.get("button")
        
        if button.isdigit() or button == ".":
            session['display'] = session.get('display', '') + button
        elif button in ["+", "-", "*", "/"]:
            session['display'] = session.get('display', '') + " " + button + " "
        elif button == "=":
            try:
                expression = session.get('display', '')
                session['display'] = str(eval(expression))
            except Exception:
                session['display'] = ""
                error = "Invalid Input"
        elif button == "C":
            session['display'] = ""
        elif button == "⌫":
            session['display'] = session.get('display', '')[:-1]

        display = session.get('display', '')

    return render(request, 'calculator/calculator.html', {'display': display, 'error': error})
