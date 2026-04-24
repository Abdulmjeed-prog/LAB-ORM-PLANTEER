from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Plant, Country
from .models import Comment
from .forms import PlantForm
from .forms import CommentForm
from django.db.models import Q, Count ,Avg 
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()
    categories = Plant.objects.values_list('category', flat=True).distinct()
    countries = Country.objects.all().order_by('name')
    selected_countries = []
    category = 'All Categories'
    edible = ''
    selected_country_objects = []

    

    if request.method == 'POST':
        category = request.POST.get('category', 'All Categories')
        edible = request.POST.get('edible', '')
        selected_countries = request.POST.getlist('countries')
        selected_country_objects = Country.objects.filter(id__in=selected_countries)

        if category != 'All Categories':
            plants = plants.filter(category=category)

        if selected_countries:
            plants = plants.filter(countries__id__in=selected_countries).distinct()
        if edible == 'yes':
            plants = plants.filter(is_edible=True)
        elif edible == 'no':
            plants = plants.filter(is_edible=False)

    plants = plants.annotate(comments_count=Count('comment'))

    page_number = request.GET.get('page',1)
    paginator = Paginator(plants,6)
    plants_page = paginator.get_page(page_number)
    return render(request, 'plants/all_plants.html', {
        'plants': plants_page,
        'categories': categories,
        'countries': countries,
        'selected_countries': selected_countries,
        'selected_category': category,
        'selected_edible': edible,
        'selected_country_objects': selected_country_objects,
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
    countries = Country.objects.all().order_by('name')
    if request.method == 'POST':
        
        plant_form = PlantForm(request.POST, request.FILES)
        if plant_form.is_valid():
            plant_form.save()
            messages.success(request,'Your plant has been added')
        else:
            messages.error(request, "Something goes wrong")
            return render(request, 'plants/add_plant.html', {
                'plant_form': plant_form,
                'categories': Plant.CategoryChoices.choices,
                'countries': countries
            })
        return redirect('main:home_view')
    return render(request, 'plants/add_plant.html',{'categories': Plant.CategoryChoices.choices, 'countries': countries})

def update_plant(request: HttpRequest, plant_id):
    plant = Plant.objects.get(pk=plant_id)
    countries = Country.objects.all().order_by('name')
    if request.method == 'POST':
        plant_form = PlantForm(request.POST, request.FILES, instance=plant)
        selected_country_ids = request.POST.getlist('countries')
        if plant_form.is_valid():
            plant_form.save()
            messages.success(request,'Your plant has been updated')
            return redirect('plants:details_view', plant_id = plant_id)
        else:
            messages.error(request, 'Something goes wrong')

        return render(request, 'plants/update_plant.html', {
            'plant': plant,
            'plant_form': plant_form,
            'categories': Plant.CategoryChoices.choices,
            'countries': countries,
            'plant_country_ids': list(plant.countries.values_list('id', flat=True)),
            'selected_country_ids': selected_country_ids,
        })

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

    try:
        plant = Plant.objects.get(pk = plant_id)
        plant.delete()
        messages.success(request, "The plant has benn deleted")
    except:
        messages.error(request, "Something goes wrong")

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


