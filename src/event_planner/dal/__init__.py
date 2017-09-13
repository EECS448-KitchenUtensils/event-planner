"""
The Database Abstraction Layer for event-planner
"""

# This looks goofy, but is needed to promote the classes contained in the 
# submodules of this package into first-class, package-level classes
from . Event import Event
from . Participant import Participant
from . TimeRange import TimeRange
