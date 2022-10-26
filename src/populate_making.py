import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'making_project.settings')

import django
django.setup()
from making.models import Category, Project

def populate():
    # Creating lists of dictionaries with the pages to add to each category
    projects = [
        {'title': 'Project 1',
        'instructions': 'Project info here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'categories': ['electronic']},
        {'title': 'Project 2',
        'instructions': 'Project info here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'categories': ['electronic', '3D printing']},
        {'title': 'Project 3',
        'instructions': 'Project info here. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'categories': ['3D printing']}

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
        c = Project.objects.get_or_create(title=p['title'], instructions=p['instructions'])[0]
        
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

