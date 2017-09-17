********************************************************************************************
EECS 448 Project 1 (Fall 2017)
********************************************************************************************

Design
====================

MVC Pattern
^^^^^^^^^^^^^
* Database Models
    * events
        * Fields
            * title: *string*
            * description: *string*
            * date: *date*
            * id: *integer, primary key*
            * admin_link: *string*
        * Relations
            * participants: *one-to-many*
    * participant
        * Fields
            * name: *string*
            * id: *integer, primary key*
            * is_admin: *boolean*
        * Relations
            * timeslots: *one-to-many*
    * timeslot
        * Fields
            * part_id: *integer, foreign key*
            * timeslot: *time*
* Views
* Controllers

Account-less authentication scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. An anonymous user creates an event
#. A session is created that owns this event
#. A 'magic link' is presented to the user to create a new session if they lose their current one. This can also be used to share ownership of an event.

Stretch Goals
=============

1. Implement the above authenication scheme
#. Add an option to email the 'magic link' upon event creation so that the user has easy access to it after they close the app.
#. Add an option to email a link to the event upon a non-owner adding their availability

Implementation
==============
* Python 3
* Flask (Views and Controllers)
* SQLAlchemy (Models)
* Postgresql (Database)
* Jinja2 (Templates)
* JQuery & JQuery UI (DOM Manipulation)
* Bootstrap 4 (CSS Framework)

