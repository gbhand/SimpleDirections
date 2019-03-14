import googlemaps
import json
from datetime import datetime
from datetime import timedelta
from pandas.io.json import json_normalize

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
total_distance = legs.get("distance").get("text")
total_duration = legs.get("duration_in_traffic").get("text")
raw_time = legs.get("duration_in_traffic").get("value")
eta = now + timedelta(seconds=raw_time)
    


if warnings == []:
    warn_out = "There are no travel warnings :)"
else:
    warn_out = warnings #TODO make this iterate through list
    
print("\n\nRoute from ", start, " to ", end, " via ", summary)
print(warn_out)
print("You should cover ", total_distance, " in ", total_duration, " arriving at ", eta.strftime("%I:%M%p"), "\n\n")

out = open("out.html", "w")
for step in legs.get("steps"):
    duration = step.get("duration").get("text")
    distance = step.get("distance").get("text")
    #instructions = step.get("html_instructions").json_normalize()
    instructions = step.get("html_instructions")
    print(instructions, file=out)
    #print("for ", duration, " | (", distance, ")", file=out)
    print("<br>", file=out)
    print(duration, " | (", distance, ")", file=out)
    print("<br>", file=out)
    print("<br>", file=out)
    

print("\n\nHave a safe trip!")


#with open("output", "w") as out:
#    out.write(str(directions))
