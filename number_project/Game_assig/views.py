from django.shortcuts import render, redirect
import random

def index(request):
    if 'number' not in request.session:
        request.session['number'] = 15#random.randint(1, 100)
        request.session['attempts'] = 0
        request.session['guesses'] = []
        request.session['flag'] = False
    print(request.session['attempts'], request.session['flag'], request.session['number'])
    message = None
    if request.method == 'POST':
        guess = int(request.POST['guess'])
        request.session['attempts'] += 1
        request.session['guesses'].append(guess)

        if guess < request.session['number']:
            message = "Too low!"
        elif guess > request.session['number']:
            message = "Too high!"
        else:
            request.session['flag'] = True
            print(request.session['attempts'], request.session['flag'], request.session['number'])
            return redirect('/winner')

        if request.session['attempts'] >= 5:
            return redirect('/loser')

    context = {
        'message': message,
        'attempts': request.session['attempts']
    }
    return render(request, 'index.html', context)

def winner(request):
    if request.method == 'POST':
        name = request.POST['name']
        winners = request.session.get('winners', [])
        winners.append({'name': name, 'attempts': request.session['attempts']})
        request.session['winners'] = winners
        # Clear session data for new game
        request.session.pop('number', None)
        request.session.pop('attempts', None)
        request.session.pop('guesses', None)
        return redirect('/leaderboard')

    context = {
        'attempts': request.session['attempts']
    }
    return render(request, 'winner.html', context)

def playagain(request):
    if request.session.get('flag', True):
        request.session['attempts'] = 0
        request.session['flag'] = False
        request.session.pop('number', None)
        request.session.pop('attempts', None)
        request.session.pop('guesses', None)
    return redirect('/')

def loser(request):
    # Clear session data for new game
    request.session.pop('number', None)
    request.session.pop('attempts', None)
    request.session.pop('guesses', None)
    return render(request, 'loser.html')

def leaderboard(request):
    # Show name of winners
    winners = request.session.get('winners', [])
    context = {
        'winners': winners
    }
    return render(request, 'leaderboard.html', context)
