import unittest
from urllib.parse import urlparse
import event_planner
from event_planner.models import *
from datetime import date

def make_slots():
    """Helper func to make the timeslot part of the form data"""
    return {"slot_%s" % i: "1" for i in range(48)}

class IntegrationTestCase(unittest.TestCase):
    """Base class for all integration tests"""
    def setUp(self):
        self.app = event_planner.app.test_client()
        self.db = event_planner.db
        with event_planner.app.app_context():
            event_planner.db.create_all()
    def tearDown(self):
        with event_planner.app.app_context():
            event_planner.db.drop_all()
        

class EventTestCase(IntegrationTestCase):
    """ Test class specific for testing events. """
    def setUp(self):
        super().setUp()
        self.slots = make_slots()
        self.text_members = ["eventname", "eventdescription", "adminname"]
        self.form_members = self.text_members + ["date"]
    
    def valid_data(self):
        """Returns a valid dictionary of form data"""
        data = {el: "testData" for el in self.text_members}
        data.update(self.slots)
        data["date"] = "12/31/2101"
        return data

class WhenAnEventIsCreatedSucessfully(EventTestCase):

    def setUp(self):
        super().setUp()
        self.slots["slot_23"] = "1"
        data=self.valid_data()
        self.res = self.app.post("/new", data=data)
    def test_status_code(self):
        """Should redirect (code 302)"""
        self.assertEqual(self.res.status_code, 302)
    def test_event_count(self):
        """Should add exactly one event to the database"""
        with event_planner.app.app_context():
            self.assertEqual(Event.query.count(), 1)
    def test_redirect_to_home(self):
        """Should redirect back to main page"""
        self.assertEqual(urlparse(self.res.location).path, "/")
    def test_retrieve_event(self):
        """The new event should be accessible from /event/<id>"""
        res = self.app.get("/event/1")
        self.assertEqual(res.status_code, 200)

class BeforeAnEventIsCreated(EventTestCase):

    def test_nonexist(self):
        """Should return a 404"""
        res = self.app.get("/event/3")
        self.assertEqual(res.status_code, 404)

class CreatingAnEventWith(EventTestCase):

    def test_missing_members(self):
        """Should return 400"""
        self.form_members.remove("eventdescription")
        for element in self.form_members:
            with self.subTest(i=element):
                res = self.missing(element)
                self.assertEqual(res.status_code, 400)
    def test_missing_timeslots(self):
        """Should return 400"""
        data = self.valid_data()
        #remove all timeslots
        tmp_data = {}
        for key, value in data.items():
            if not key.startswith("slot"):
                tmp_data[key] = value
        data = tmp_data
        res = self.app.post("/new", data=data)
        self.assertEqual(res.status_code, 400)
    def test_empty_timeslots(self):
        data = self.valid_data()
        for key, value in data.items():
            if key.startswith("slot"):
                data[key] = "0"
        res = self.app.post("/event/1", data=data)
        self.assertEqual(res.status_code, 400)
    def test_empty_members(self):
        """Should return 400"""
        self.form_members.remove("eventdescription") #eventdescription is allowed to be empty
        for element in self.form_members:
            with self.subTest(i=element):
                res = self.empty(element)
                self.assertEqual(res.status_code, 400)
    def missing(self, element):
        """Executes a form submission, minus the given form member"""
        data = self.valid_data()
        del data[element]
        return self.app.post("/new", data=data)
    def empty(self, element):
        """Executes a form submissing with the given field as empty string"""
        data = self.valid_data()
        data[element] = ""
        return self.app.post("/new", data=data)

class ParticipantTestCase(IntegrationTestCase):
    """ Test class specific to testing participants """
    def setUp(self):
        super().setUp()
        self.slots = make_slots()
        self.text_members = ["participantname"]
        self.form_members = self.text_members
        with event_planner.app.app_context():
            self.event = event_planner.models.Event("test", "test", date(2015, 10, 10))
            self.db.session.add(self.event)
            self.db.session.commit()
    
    def valid_data(self):
        """Returns a valid dictionary of form data"""
        data = {el: "testData" for el in self.text_members}
        data.update(self.slots)
        return data

class WhenAParticipantIsAddedSuccessfully(ParticipantTestCase):
    def setUp(self):
        super().setUp()
        self.slots["slot_23"] = "1"
        data=self.valid_data()
        self.res = self.app.post("/event/1", data=data)
    def test_status_code(self):
        """Should redirect (code 302)"""
        self.assertEqual(self.res.status_code, 302)
    def test_participant_count(self):
        """Should add exactly one participant to the event"""
        with event_planner.app.app_context():
            self.assertEqual(len(Event.query.first().participants), 1)
    def test_redirect_to_current_event(self):
        """Should redirect back to the current event"""
        self.assertEqual(urlparse(self.res.location).path, "/event/1")

class CreatingAParticipantWith(ParticipantTestCase):
    def test_missing_members(self):
        """Should return 400"""
        for element in self.form_members:
            with self.subTest(i=element):
                res = self.missing(element)
                self.assertEqual(res.status_code, 400)
    def test_missing_timeslots(self):
        """Should return 400"""
        data = self.valid_data()
        #remove all timeslots
        tmp_data = {}
        for key, value in data.items():
            if not key.startswith("slot"):
                tmp_data[key] = value
        data = tmp_data
        res = self.app.post("/event/1", data=data)
        self.assertEqual(res.status_code, 400)
    def test_empty_timeslots(self):
        data = self.valid_data()
        for key, value in data.items():
            if key.startswith("slot"):
                data[key] = "0"
        res = self.app.post("/event/1", data=data)
        self.assertEqual(res.status_code, 400)
    def test_empty_members(self):
        """Should return 400""" 
        for element in self.form_members:
            with self.subTest(i=element):
                res = self.empty(element)
                self.assertEqual(res.status_code, 400)
    def missing(self, element):
        """Executes a form submission, minus the given form member"""
        data = self.valid_data()
        del data[element]
        return self.app.post("/event/1", data=data)
    def empty(self, element):
        """Executes a form submissing with the given field as empty string"""
        data = self.valid_data()
        data[element] = ""
        return self.app.post("/event/1", data=data)


    

