********************************************************************************************
EECS 448 Project 1 (Fall 2017)
********************************************************************************************

Design
====================

MMVC Pattern
^^^^^^^^^^^^^
* Database Models
    * events
        * Fields
            * title: *string*
            * description: *string*
            * date: *datetime*
            * id: *uuid, primary key*
            * admin_link: *string*
        * Relations
            * event_timeslots: *one-to-many*
            * participants: *one-to-many*
    * event_timeslots
        * Fields
            * event_id: *uuid, foreign key*
            * timeslot: *enum(Timeslot)*
    * participants
        * Fields
            * name: *string*
            * id: *uuid, primary key*
        * Relations
            * participant_timeslots: *one-to-many*
    * participant_timeslots
        * Fields
            * part_id: *uuid, foreign key*
            * timeslot: *enum(Timeslot)*
* Application Models
    * Event
        * Properties
            * admin_link
            * title
            * description
        * Instance methods
            * setters for properties
            * getter for related participants
            * setter for relating participants
        * Static methods
            * Get all events
            * 
    * Participant
        * Properties
            * name
            * timeslots
        * Instance methods
            * setter for timeslots
* Views
* Controllers

Account-less authentication scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. An anonymous user creates an event
#. A session is created that owns this event
#. A 'magic link' is presented to the user to create a new session if they lose their current one. This can also be used to share ownership of an event.

Stretch Goals
=============

1. Add an option to email the 'magic link' upon event creation so that the user has easy access to it after they close the app.
#. Add an option to email a link to the event upon a non-owner adding their availability

Implementation
==============
* Python 3
* Flask (Views and Controllers)
* SQLAlchemy (Models)
* SQLite3 (Database)
* Jinja2 (Templates)
* JQuery & JQuery UI (DOM Manipulation)
* Bootstrap 4 (CSS Framework)

