from domain.events.handler_config import HANDLER_CONFIG

_registered_events = {}

def register_event(event, event_handler):
    if not _registered_events.get(event):
        _registered_events[event] = []
    _registered_events[event].append(event_handler)
    
def dispatch_event(event):
    event_type = type(event)
    for event_handler in _registered_events.get(event_type, []):
        event_handler(event)

def register_from_config():
    for event, handlers in HANDLER_CONFIG.items():
        for handler in handlers:
            register_event(event, handler)

    
