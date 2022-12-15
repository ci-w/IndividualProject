import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'making_project.settings')

import django
django.setup()
from making.models import Category, Project

def populate():
    # Creating lists of dictionaries with the pages to add to each category
    projects = [
        {'title': 'Light up card',
        'description': 'Use paper electronics to create a beautiful light-up greeting card.',
        'instructions': 'You will need: card, LEDs, tape, scissors. Create a design on the card. Create holes in the card with the scissors for the LEDs. Thread through the LEDs through the holes. Secure them with the tape. Sort out the wires. Present the card.',
        'categories': ['electronic']},
        {'title': 'Braille dice',
        'description': '3D print a set of dice that have braille numbers.',
        'instructions': 'You will need: a 3D printer, printer filament of choice, sandpaper. Download the dice files. Load them up in the 3D printer. Load up the filament. Set it to print the dice. Sand printed dice if needed.',
        'categories': ['3D printing']},
        {'title': 'Creature',
        'description': 'Create a 3D printed creature with light up eyes.',
        'instructions': 'You will need: a 3D printer, LEDs, sandpaper, printer filament, tape. Download the creature file. Load file into printer. Load filament into printer. Print the file. Sand edges of finished creature if needed. Put LEDs through the eye holes. Tape the wiring to the inside of the creature. ',
        'categories': ['electronic','3D printing']}
    ]

    # List of all the different categories
    cats = ['3D printing', 'electronic']

    def add_cat(name):
        c = Category.objects.get_or_create(category=name)[0]
        c.save()

    # Creates categories
    for cat in cats:
        print("Adding category " + cat)
        add_cat(cat)
    

    def add_project(p):
        c = Project.objects.get_or_create(title=p['title'], description=p['description'], instructions=p['instructions'])[0]
        
        c.save()

        #c.category.add(Category.objects.get(category="electronic"))
        #print(c.category.all())

        for i in p['categories']:
            c.category.add(Category.objects.get(category=i))
        
        """ c.save()
        print("Adding project " + p['title'])
        for i in p['categories']:
            print("Linking category " + i)
            categoryobject = Category.objects.get(category=i)
            print(categoryobject)
            c.category.add(categoryobject)  
            c.save()
            print(c.category)
            print("below this:")
            print(c) """
            
    
    for p in projects:
        add_project(p)
        print("added project " + p['title'])
    

    
    
    
      

if __name__ == '__main__':
    print('Starting Making population script...')
    populate()

