import googlemaps
import json
from datetime import datetime
from datetime import timedelta

API_KEY = open("config", "r").read() #don't steal my key plz
gmaps = googlemaps.Client(key=API_KEY)

#TODO delete
#start = "11115 Collegio Dr"
#end = "Regents Road West Lot"
start = input("Enter starting address: ")
#sanitize information and verify validity
#maybe use OpenStreetMap?
end = input("Enter destination address: ")
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
distance = legs.get("distance").get("text")
duration = legs.get("duration_in_traffic").get("text")
raw_time = legs.get("duration_in_traffic").get("value")
eta = now + timedelta(seconds=raw_time)

if warnings == []:
    warn_out = "There are no travel warnings :)"
else:
    warn_out = warnings #TODO make this iterate through list
    
print("\n\nRoute from ", start, " to ", end, " via ", summary)
print(warn_out)
print("You should cover ", distance, " in ", duration, " arriving at ", eta.strftime("%I:%M%p"))
print("\n\nHave a safe trip!")


#with open("output", "w") as out:
#    out.write(str(directions))
