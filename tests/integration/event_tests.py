import unittest
from urllib.parse import urlparse
import event_planner
from event_planner.models import *

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
class WhenAnEventIsCreated(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self.slots = {"slot_%s" % i: "0" for i in range(48)}
        self.slots["slot_23"] = "1"
        data=dict(
            eventname="testevent",
            eventdescription="testdescription",
            adminname="testadmin",
            date="11/21/201",
            )
        data.update(self.slots)
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
class BeforeAnEventIsCreated(IntegrationTestCase):
    
    def test_nonexist(self):
        """Should return a 404"""
        res = self.app.get("/event/3")
        self.assertEqual(res.status_code, 404)