For Friday: project page view adapts depending on user's requirements.
Make modifications to the site as they come up.
___
## Background
Go through each section of the "lit review"
For Friday: have each section, summary of what will be in each.

## Requirements/Analysis
Look at notes from earlier in year at what I was wanting to make. What is my item meant to DO
Friday: summary of what will be here.
These headings/sections will then be repeated in design/implementation.

## Design
Design of how I will fulfil those requirements

## Implementation
How I implemented that design

## EVALUATION
Friday: write eval plan
What am i looking to evaluate:
- the idea of it? like do people actually think its needed/useful
- the execution of it. does it successfully do what its meant to be doing
- the design of it
- does it address the key things i/they are looking for
	How good is your solution?
	How well did you solve the general problem and what evidence do you
	have to support that?
Looking at the "aims" section and then asking specific questions to find out if we achieved that. 

Experimental design:
This will obviously depend on what I can actually do. dear lord grant me the strength

Pre-questionnaire:
(getting an idea of who this person is)
- What is your experience in:
    - making
        - do you use online resources to get Making project tutorials?
    - makerspaces
    - working with people that have:
        - intellectual disabilities
        - cognitive impairments
        - other disabilities 

"Demo":
- look at site
- maybe have a list of tasks for them to do?

Main questions:
- Would this tool lower the barriers to entry? I.e. does it make it easier for disabled people to do Making projects
    - have a question for each barrier 
- Does it show tutorials in an accessible way?
    - Specify further i.e. "readability/information easy to understand/"
- Does it allow a user to improve their skills over a customised course of projects?
    - Do you think doing these projects would improve their skills 

___
## Motivation
- get disabled people to improve their skills (specific) through tangible learning
- lower the barriers to entry for this ^ by designing a system that would allow them to find/complete tangible learning projects that are accessible to their needs
- improving their skills over a course of projects
- in a way that is designed to overcome issues they may have with "traditional" learning i.e. having the site/tutorials adapt to them rather than the other way around


_______
I have it structured in such a way that in the future it'll be easy to add multiple requirement objects per project/person (i.e. checking tool duplicacy per requirements object rather than profile/project)



<h3>
      {% block page_title %}
      Homepage
      {% endblock %}
      </h3>    
      {% if user.is_authenticated %}
        You are logged in as: {{ user.username }} <br>
        {% if user_profile %} 
          Current user profile is: {{ user_profile.profile_name }} <br>
        {% endif %}
      {% endif %}

    {% block body_block %}
          Welcome to Making Projects!
          <img src="{% static 'making/images/projects/18/creature.png' %}" alt="My image">
    {% endblock %}
    