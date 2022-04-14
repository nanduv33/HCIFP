from django.shortcuts import render
from coloring.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_author_by_name(authorname): 
  author = None
  
  # check if an Author with name 'authorname' already exists
  if Author.objects.filter(name = authorname).exists():
    # if so, fetch that object from the database
    author = Author.objects.get(name=authorname)
    
  else: 
    # otherwise, create a new Author with the name authorname
    author = Author(name = authorname)
    # save the created object
    author.save()

  return author

def get_drawing_by_title(title, authorkey, jsondata):
  drawing = None
  if Drawing.objects.filter(author = authorkey).exists():
    # if so, fetch that object from the database
      Drawing.objects.filter(author = authorkey).update(title = title, drawing=jsondata)
      drawing = Drawing.objects.get(title=title, author=authorkey)
    
  else: 
      drawing = Drawing(title = title, author = authorkey, drawing=jsondata)
      # save the created object
      drawing.save()

  return drawing
  



@csrf_exempt
def index(request, authorname="DefaultAuthor", titlename="DefaultTitle"):

  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  drawing = None
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    data1 = json.loads(request.body)
    print(data)
    print("data1", data1)
    drawing = get_drawing_by_title(data["title"], author, data1)
    print("The drawing is: ", drawing)
    print("The drawing title is: ", drawing.title)

    # find out if a Drawing with the Author and Title already exists?
    # if it doesn't exist, you may create a new Drawing object
    # if it does exist, you may update an existing Drawing object
    # make sure to save your object after creating or updating 
    # for more information, see get_author_by_name() and reference below
    # https://docs.djangoproject.com/en/4.0/ref/models/instances/#saving-objects
    
    return HttpResponse(True)

  else: 
    # GET request received
    points = []
    if Drawing.objects.filter(author = author).exists():
    # if so, fetch that object from the database
      drawing = Drawing.objects.get(author=author)
      data = drawing.drawing
      points = data["points"]
      # print("Drawing points", drawing.drawing)

    # if a drawing by the author already exists,
    # send the drawing conent and title with the data below
    
    data = {
      "author": author,
      "drawing": drawing,
      "drawingPath": points
    }
    
    return render(request, 'coloring/index.html', data)