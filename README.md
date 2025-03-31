# Generation of Simulated Data for Apple Supply Chain 
This project is an approach to show Vibe Coding principles. Using only prompts, get the LLM to do deep research, and then use all of that researched data into creating synthetic data to learn how to handle supply chain disruptions.

## Approach Taken

1. **Identification of Apple Varieties**
   - Selected the top five apple varieties consumed in Germany:
     - Royal Gala
     - Fuji
     - Granny Smith
     - Golden Delicious
     - Pink Lady

2. **Definition of Product Data**
   - Defined attributes such as:
     - Apple Variety
     - Shelf Life
     - Grade
     - Unit of Measure

3. **Harvest Season Data Collection**
   - Gathered harvest season data by country and variety.

4. **Production Tonnage Estimation**
   - Identified the approximate production tonnage per country and variety.

5. **Yield Breakup Generation**
   - Created a yield distribution based on:
     - Harvest season
     - Country
     - Variety
     - Tonnage

6. **Supplier Data Compilation**
   - Collected supplier information for each country.

7. **Nearest Shipping Ports Identification**
   - Determined the nearest ports from which suppliers would ship apples.

8. **Supermarket Chain & Consumption Analysis**
   - Identified the top three supermarket chains in Germany that stock the top five varieties.
   - Determined the top three cities with the highest apple consumption.

9. **Sales Estimation per City and Supermarket**
   - Estimated apple sales per city and supermarket chain, considering:
     - Demand
     - Seasonality
     - Variety preferences
     - City population

10. **Warehouse Identification**
    - For each identified city and supermarket chain, determined the largest warehouse in that city.

11. **Importer Data Analysis**
    - Researched importers in Rotterdam and identified the largest apple importer with a cold storage facility.

12. **Energy & Sustainability Research**
    - Analyzed energy and sustainability data for the cold storage facility (Cool Port II, Rotterdam).
    - Collected energy-related data, including:
      - Storage Facility
      - Address
      - Total Energy Consumed
      - Backup Energy
      - Total Capacity Tonnage
      - Solar Generation Capacity

13. **Energy Consumption Calculation**
    - Estimated energy consumption for each journey from the origin port to the destination port for various shipping routes.
14. **Order Generation**
    - Write a program that simulates and creates orders by matching Supply and Demand
16. **Introduce Chaos**
    - Identify major events during the year that might impact supply, transit and demand (the events can be natural disasters, labour issues, technology related etc)
    - Adjust the delivery dates and quantities accordingly

