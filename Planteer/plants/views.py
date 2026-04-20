from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Plant
from .models import Comment
from .forms import PlantForm
from .forms import CommentForm
from django.db.models import Q
# Create your views here.

def all_plants_view(request:HttpRequest):
    plants = Plant.objects.all()
    categories = Plant.objects.values_list('category', flat=True).distinct()

    if request.method == 'POST':
        category = request.POST['category']
        edible = request.POST['edible']
        
        if category != 'All Categories':
            plants = plants.filter(category=category)
        if edible == 'yes':
            plants = plants.filter(is_edible=True)
        elif edible == 'no':
            plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html',{'plants': plants, 'categories': categories})

def details_view(request:HttpRequest, plant_id):
    plant = Plant.objects.get(pk = plant_id)
    recom_plants = Plant.objects.filter(category = plant.category)
    recom_plants = recom_plants.exclude(pk = plant_id)
    recom_plants = recom_plants.order_by('?')[:3]
    comments = Comment.objects.filter(plant_id=plant).order_by('-create_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.plant_id = plant
            form.save()
        else:
            return render(request, 'plants/details.html', {
                'plant': plant,
                'recom_plants': recom_plants,
                'comments': comments,
                'comment_form': comment_form
            })

            
    return render(request,'plants/details.html', {'plant': plant, 'recom_plants': recom_plants,'comments': comments})

def add_plant(request:HttpRequest):
    
    if request.method == 'POST':

        plant_form = PlantForm(request.POST, request.FILES)
        if plant_form.is_valid():
            plant_form.save()
        else:
            return render(request, 'plants/add_plant.html', {
                'plant_form': plant_form,
                'categories': Plant.CategoryChoices.choices
            })
        return redirect('main:home_view')
    return render(request, 'plants/add_plant.html',{'categories': Plant.CategoryChoices.choices})

def update_plant(request: HttpRequest, plant_id):
    plant = Plant.objects.get(pk=plant_id)

    if request.method == 'POST':
        plant_form = PlantForm(request.POST, request.FILES, instance=plant)

        if plant_form.is_valid():
            plant_form.save()
            return redirect('plants:details_view', plant_id = plant_id)

        # form is invalid → show errors back in the same template
        return render(request, 'plants/update_plant.html', {
            'plant': plant,
            'plant_form': plant_form,
            'categories': Plant.CategoryChoices.choices,
        })

    # GET: show form filled with current plant
    plant_form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {
        'plant': plant,
        'plant_form': plant_form,
        'categories': Plant.CategoryChoices.choices,
    })

def delete_plant(request:HttpRequest, plant_id):

    plant = Plant.objects.get(pk = plant_id)
    plant.delete()

    return redirect('plants:all_plants_view')

def search_plant(request: HttpRequest):
    query = request.GET.get('q', '').strip()
    plants = Plant.objects.none()

    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(used_for__icontains=query)
        ).distinct()

    return render(request, 'plants/search_plant.html', {
        'query': query,
        'plants': plants,
    })


