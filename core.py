import googlemaps
import json
from datetime import datetime
from datetime import timedelta

API_KEY = open("config", "r").read() #don't steal my key plz
gmaps = googlemaps.Client(key=API_KEY)

def join(*args):
    out = ""
    for arg in args:
        out = out + str(arg)
        
    return out


def find_route(waypoints):
    
    start = waypoints[0]
    end = waypoints[1]
    
    now = datetime.now()
    list = gmaps.directions(
        start,
        end,
        mode="driving",
        departure_time=now,
        traffic_model="pessimistic") #ain't trying to give false hope
                #best_guess (average of live & historical), optimistic, pessimistic
    data = list[0]
    
    summary = data.get("summary")
    warnings = data.get("warnings")
    
    legs = data.get("legs")[0]
    total_distance = legs.get("distance").get("text")
    total_duration = legs.get("duration_in_traffic").get("text")
    raw_time = legs.get("duration_in_traffic").get("value")
    eta = now + timedelta(seconds=raw_time)
        
    
    
    if warnings == []:
        warn_out = "There are no travel warnings :)"
    else:
        warn_out = warnings #TODO make this iterate through list
    
    
    
    route = join("Route from ", start, " to ", end, " via ", summary, "")
    warn = join(warn_out)
    info_distance = join("You should cover ", total_distance, " in ", total_duration, " arriving at ", eta.strftime("%I:%M%p"), "")
    
    info = [route, warn, info_distance]
    steps = []
    
    for step in legs.get("steps"):
        duration = step.get("duration").get("text")
        distance = step.get("distance").get("text")
        instructions = step.get("html_instructions")
        
        step_text = instructions.replace("<b>", "").replace("</b>", "")
        step_distance = join(duration, " | (", distance, ")")

        entry = {"text": step_text, "distance": step_distance}
        steps.append(entry)
        
    output = {"info": info, "steps": steps}
    
    #printw("Have a safe trip!")
    return output
    
