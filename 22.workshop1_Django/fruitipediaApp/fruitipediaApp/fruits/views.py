from django.shortcuts import render, redirect
from fruitipediaApp.fruits.models import Fruit
from fruitipediaApp.fruits.forms import CategoryCreateForm, FruitCreateForm

# Create your views here.


def index(request):
    return render(request, 'common/index.html')


def dashboard(request):
    fruits = Fruit.objects.all()

    context = {
        'fruits': fruits,
    }

    return render(request, 'common/dashboard.html', context)


def create_fruit(request):
    if request.method == 'GET':
        form = FruitCreateForm()
    elif request.method == 'POST':
        form = FruitCreateForm(
            request.POST,
        )

        if form.is_valid():
            form.save()
            print('Success!')

            return redirect('dashboard')
    else:
        pass

    context = {
        'form': form,
    }

    return render(request, 'fruits/create-fruit.html', context)


def details_fruit(request, fruit_id):
    fruit = Fruit.objects.filter(pk=fruit_id).get()

    context = {
        'fruit': fruit,
    }

    return render(request, 'fruits/details-fruit.html', context)


def edit_fruit(request, fruit_id):
    fruit = Fruit.objects.filter(pk=fruit_id).get()

    if request.method == 'GET':
        form = FruitCreateForm(
            instance=fruit,
        )
    elif request.method == 'POST':
        form = FruitCreateForm(
            request.POST,
            instance=fruit,
        )

        if form.is_valid():
            form.save()
            print('Success!')

            return redirect('dashboard')
        else:
            pass

        context = {
            'form': form,
            'fruit': fruit,
        }

    return render(request, 'fruits/edit-fruit.html', context)


def delete_fruit(request, fruit_id):
    fruit = Fruit.objects.filter(pk=fruit_id).get()

    if request.method == 'GET':
        form = FruitCreateForm(
            instance=fruit,
        )
    elif request.method == 'POST':
        form = FruitCreateForm(
            request.POST,
            instance=fruit,
        )

        if form.is_valid():
            form.save()
            print('Success!')

            return redirect('dashboard')
        else:
            pass

        context = {
            'form': form,
            'fruit': fruit,
        }

    return render(request, 'fruits/delete-fruit.html', context)


def create_category(request):
    if request.method == 'GET':
        form = CategoryCreateForm()
    elif request.method == 'POST':
        form = CategoryCreateForm(
            request.POST,
        )

        if form.is_valid():
            form.save()
            print('Success!')

            return redirect('create-category')
    else:
        pass

    context = {
        'form': form,
    }

    return render(request, 'categories/create-category.html', context)
