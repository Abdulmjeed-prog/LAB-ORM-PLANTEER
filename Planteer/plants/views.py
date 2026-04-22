from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Plant, Country
from .models import Comment
from .forms import PlantForm
from .forms import CommentForm
from django.db.models import Q
# Create your views here.

def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()
    categories = Plant.objects.values_list('category', flat=True).distinct()
    countries = Country.objects.all()
    selected_countries = []
    category = 'All Categories'
    edible = ''

    if request.method == 'POST':
        category = request.POST.get('category', 'All Categories')
        edible = request.POST.get('edible', '')
        selected_countries = request.POST.getlist('countries')

        if category != 'All Categories':
            plants = plants.filter(category=category)

        if selected_countries:
            plants = plants.filter(countries__id__in=selected_countries)
        if edible == 'yes':
            plants = plants.filter(is_edible=True)
        elif edible == 'no':
            plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': categories,
        'countries': countries,
        'selected_countries': selected_countries,
        'selected_category': category,
        'selected_edible': edible,
    })

def details_view(request:HttpRequest, plant_id):
    plant = Plant.objects.get(pk = plant_id)
    print(plant.countries.all)
    recom_plants = Plant.objects.filter(category = plant.category)
    recom_plants = recom_plants.exclude(pk = plant_id)
    recom_plants = recom_plants.order_by('?')[:3]
    comments = Comment.objects.filter(plant_id=plant).order_by('-create_at')


    # Add_comment
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.plant_id = plant
            form.save()
        else:
            print(comment_form.errors)

    return render(request,'plants/details.html', {'selected_plant': plant, 'plants': recom_plants,'comments': comments})

def add_plant(request:HttpRequest):
    countries = Country.objects.all()
    if request.method == 'POST':

        plant_form = PlantForm(request.POST, request.FILES)
        if plant_form.is_valid():
            plant_form.save()
        else:
            print(plant_form.errors)
            return render(request, 'plants/add_plant.html', {
                'plant_form': plant_form,
                'categories': Plant.CategoryChoices.choices,
                'countries': countries
            })
        return redirect('main:home_view')
    return render(request, 'plants/add_plant.html',{'categories': Plant.CategoryChoices.choices, 'countries': countries})

def update_plant(request: HttpRequest, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    countries = Country.objects.all()
    if request.method == 'POST':
        plant_form = PlantForm(request.POST, request.FILES, instance=plant)
        selected_country_ids = request.POST.getlist('countries')
        if plant_form.is_valid():
            plant_form.save()
            return redirect('plants:details_view', plant_id = plant_id)
        else:
            print(plant_form.errors)

        # form is invalid → show errors back in the same template
        return render(request, 'plants/update_plant.html', {
            'plant': plant,
            'plant_form': plant_form,
            'categories': Plant.CategoryChoices.choices,
            'countries': countries,
            'plant_country_ids': list(plant.countries.values_list('id', flat=True)),
            'selected_country_ids': selected_country_ids,
        })

    # GET: show form filled with current plant
    plant_form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {
        'plant': plant,
        'plant_form': plant_form,
        'categories': Plant.CategoryChoices.choices,
        'countries': countries,
        'plant_country_ids': list(plant.countries.values_list('id', flat=True)),
        'selected_country_ids': [],
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
            Q(used_for__icontains=query) |
            Q(countries__name__icontains=query)
        ).distinct()

    return render(request, 'plants/search_plant.html', {
        'query': query,
        'plants': plants,
    })

def country_detail(request:HttpRequest, country_id):

    country = Country.objects.get(pk=country_id)
    country_plants = country.plant_set.all()
    print(country_plants)
    return render(request, 'plants/country_detail.html',{'plants': country_plants, 'country': country})


