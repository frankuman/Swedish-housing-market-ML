"""
Oliver Bölin
BTH, 2024
Flask frontend
"""
from flask import Flask, render_template, request, jsonify, redirect,url_for
import json
from geopy.geocoders import Nominatim
import ssl
import geopy.geocoders
import vm
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def start():
    """
    For GET requests, display the form. 
    For POSTS, get the current form.
    """
    message = ""
    print(request.method)
    # this is just flask stuff
    if request.method == 'POST':
        # Get form data
        adress = request.form.get('address', '')
        property_type = request.form.get('property_type', '')
        build_year = request.form.get('build_year', '')
        living_area = request.form.get('living_area', '')
        land_area = request.form.get('land_area', '')
        county = request.form.get('county', '')
        fee = request.form.get('fee', '')
        rooms = request.form.get('rooms', '')
        balcony = request.form.get('balcony', '')
        # check that all data is there
        if (adress and property_type and build_year and living_area and
                land_area and county and fee and rooms and balcony):
            print("Form data:", {
                "adress": adress,
                "property_type": property_type,
                "build_year": build_year,
                "living_area": living_area,
                "land_area": land_area,
                "county": county,
                "fee": fee,
                "rooms": rooms,
                "balcony": balcony
            })
            with open("data/population_density_data.json", encoding="utf-8") as data:
                population_density_data = json.load(data)
            regions = population_density_data["dimension"]["Region"]["category"]["label"]
            densities = population_density_data["value"]
            region_density_mapping = dict(zip(regions.values(), densities))
            county = county.lower().strip()

            region_density_mapping = {key.lower().strip(): value for key, value in region_density_mapping.items()}
            population_density = region_density_mapping.get(county, None)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            geolocator = Nominatim(user_agent='VarderingsMaskinen', ssl_context=ctx, adapter_factory=geopy.adapters.URLLibAdapter)
            full_address = f"{county}, {adress}"

            # geocode it
            location = geolocator.geocode(full_address)
            
            if location:
                latitude = location.latitude
                longitude = location.longitude
                display_name = location.raw.get('display_name', '')
                print(display_name)
                area_parts = display_name.split(', ')
                if len(area_parts) >= 4:    #the result always depends, [2] can be the street, town, or county
                    area = area_parts[2]
                    area = area.lower().strip()
                else:
                    area = county
                #since the population density user _ instead of " ", we need to convert the user input
                area = area.replace(' ', '_')
                area_parts = area.split('-')
                if area_parts:
                    area = area_parts[0]
                print(area)
                print(f"Latitude: {latitude}, Longitude: {longitude}")
                user_input = {
                    "property_type": property_type,
                    "build_year": build_year,
                    "living_area": living_area,
                    "land_area": land_area,
                    "county": county,
                    "area": area,
                    "latitude": latitude,
                    "longitude": longitude,
                    "fee": fee,
                    "rooms": rooms,
                    "balcony": balcony,
                    "age": 1,
                    "population_density": population_density
                }
                low_p, med_p, high_p = vm.run_model(user_input) #run the model on the result
                return redirect(url_for('evaluate', high_p=high_p, med_p=med_p, low_p=low_p, user_input=user_input,adress=adress, property_type=property_type, build_year=build_year,
                           living_area=living_area, county=county, land_area=land_area, area=area, fee=fee, rooms=rooms,
                           balcony=balcony, population_density=population_density))

            else:
                message = "Unable to geocode the address:" + full_address
        else:
            message = "All fields are required. Please fill out the entire form."
    adress = ""
    property_type = ""
    build_year = ""
    living_area = ""
    land_area = ""
    county = ""
    area = ""
    fee = ""
    rooms = ""
    balcony = ""
    return render_template('index.html', adress=adress, property_type=property_type, build_year=build_year,
                           living_area=living_area, county=county, land_area=land_area, area=area, fee=fee, rooms=rooms,
                           balcony=balcony, message=message)

@app.route("/evaluation", methods=['POST', 'GET'])
def evaluate():
    """
    Request site for dashboard
    Returns:
        template: 
    """
    # this is mostly just for show
    high_p = request.args.get('high_p', '')
    med_p = request.args.get('med_p', '')
    low_p = request.args.get('low_p', '')
    user_input = request.args.get('user_input', '')
    adress = request.args.get('adress', '')
    property_type = request.args.get('property_type', '')
    build_year = request.args.get('build_year', '')
    living_area = request.args.get('living_area', '')
    land_area = request.args.get('land_area', '')
    county = request.args.get('county', '')
    area = request.args.get('area', '')
    fee = request.args.get('fee', '')
    rooms = request.args.get('rooms', '')
    balcony = request.args.get('balcony', '')
    population_density = request.args.get('population_density', '')
    amount1 = int(low_p)
    amount2 = int(med_p)
    amount3 = int(high_p)
    low_p = "{:,.0f}".format(amount1).replace(",", " ")
    med_p = "{:,.0f}".format(amount2).replace(",", " ")
    high_p = "{:,.0f}".format(amount3).replace(",", " ")


    return render_template('results.html', high_p=high_p, med_p=med_p, low_p=low_p, user_input=user_input,adress=adress, property_type=property_type, build_year=build_year,
                           living_area=living_area, county=county, land_area=land_area, area=area, fee=fee, rooms=rooms,
                           balcony=balcony, population_density=population_density)