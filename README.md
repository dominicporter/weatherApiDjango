# Coding Task

## Overview
Your task is to implement a mostly complete mini-project. The goal is to see that you know how a project is put together and have the skills
and experience to implement some basic functionality. The project description is open-ended, but you should not take more than 3 hours on
implementation. In this time you will not be able to implement every feature you can think of, so you will have to leave functionality out. This
is intentional, we do not want you to take a week writing a perfect project, we want to see what you can achieve in a limited time with an
limited specification.
You may use google and any other development tools you normally use. You may not ask someone or something else to write any of the
code for you. You may be asked specific answers about your code in a follow-up interview.

## Deliverables
1. The code in any form you prefer, eg zip, github link etc.
2. Actual time taken from start to finish
3. A brief description of your thought process during development, including limitations, known bugs, wishlist.
4. If your code executes, then an output of some sort, eg a test result. This will help where we couldn’t run your code to see that in your
environment it did execute correctly.

## Technical information
The project should use the technologies listed below. If you do not know a particular technology, you may still proceed without it if you feel
you could learn it quickly and that your other skills indicate strong abilities to compensate. In all cases, a brief justification as part of the
project submission will be helpful.

- django
- django-rest-framework
- database: ideally postgres or sqlite
- docker
- connection to a third party api
- automated tests

## Project specification
A company is building a holiday planner. Customers can choose a sequence of destinations as a schedule, taking the weather at each
location into account.
Your task is to implement an API which could be used by a frontend (note: don’t write a front-end) to enable this functionality.
The weather information can come from any third party api, for example like this one: 🌦️ Docs | Open-Meteo.com

## Planning
User Story:
As a developer
I want an API that gives me some weather info about locations
So that I can build a website which shows this

### Objectives
- Set up the framework
- Add TDD mechanism
- Create GET endpoint which fetches weather info about a given lat/long or place name

## Progress
- [X] Django framework running in Docker

I have never used Django before so bit of pre-reading was necessary. Mostly boiler plate generated with:
```
django-admin startproject myproject
python manage.py startapp myapp
```

- [X] Add Test framework

Turns out there's already some boilerplate for tests. Set up a sample using `APITestCase`

- [X] Learn how to fetch data from open-meto.com

Simple GET request to an unauthenticated API, which takes a params record with lat/long and other argument.
There is an openmeto library to wrap the calls and do caching/retries etc but for now just keeping it simple with `requests`.
Docs here: https://open-meteo.com/en/docs

- [X] GET endpoint which takes lat/long query params and returns weather JSON on that location

To start with just getting current weather and dumping out the JSON.

- [X] Cities: query param with City name using a few hardcoded city names/latlong lookups

- [X] Country lookup - on receiving an unknown country name try to get its latlong from another API

Using Nominatim API - free, open and seems to work.

Just noticed that open-meto also has a Geocoder... one for next time.

- [X] Lazy loading / caching countries - store country locations in a DB table

So, using a DB as a cache isn't the most clever thing really but it seemed an obvious way to learn a bit about how Django DB interaction works. If I actually wanted a cache, there are lots of libraries that do this more sensibly, including one built into the open-meteo libary. Also I couldn't think of a more useful thing to stick in the DB right now.

## Further ideas
I noticed that lib-meteo has a Climate Change API, so in the context of a holiday destination planner it might be useful to calculate some info about how badly a destination has been affected, or is likely to be affected in the future. For example, we could calculate current temperature rise above pre-industrial levels at that location, CO2 PPM, PM2.5 levels or likelihood of flooding. This is all available in open-meteo and would just need some data aggregation, probably using `pandas`.

## Installation
Provide instructions on how to set up the project locally.

```bash
git clone https://github.com/yourusername/yourproject.git

cd yourproject

docker-compose build

```

## Usage

```bash
# Run the project
docker-compose start
```

Go to http://localhost:8000/api/hello/

## Testing

```bash
docker-compose run web python manage.py test weatherapp
```