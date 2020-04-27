# Association-Rule-Mining


## Collaborators
- Lillian Zha (lz2527)
- Emily Hao (esh2160)

## Files Submitted 
- README.md
- processed_motor_collisions.csv 
- association_rules.py
- example-run.txt

## Run Instructions 

 Run the following command in the directory containing the python file and the integrated csv dataset. 

 ```python3 association_rules.py processed_motor_collisions.csv <min_sup> <min_conf>```


## Chosen NYC Open Data data set 

We chose to do analysis on the 'Motor Vehicle Collisions - Person' data set found [here](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu) as the origin of our Integrated Dataset. Each row or bucket in this dataset records a person involved in a 'police reported motor vehicle collisions in NYC' beginning from 2016 until present (2020). These reports are made when 'someone is injured or killed, or where there is at least $1000 worth of damage'. 

## Motivation for choosing the Motor Collisions data set 

We attempted the association rule extraction on a few other data sets before ultimately choosing this one, including the [2018 Squirrel Census](https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw), the  [Energy and Water data Disclosure for Local Law 84-2019](https://data.cityofnewyork.us/Environment/Energy-and-Water-Data-Disclosure-for-Local-Law-84-/vdzd-yy49) and the [HIV/Aids Diagnoses by Neighborhood, Sex and Race/Ethnicity](https://data.cityofnewyork.us/Health/HIV-AIDS-Diagnoses-by-Neighborhood-Sex-and-Race-Et/ykvb-493p), however we found that the Motor Collisions data was the most intuitively mapped to meaningful buckets/items. It was also the most flexible for data processing. By this we mean that it was possible to reduce it to a manageable dataset size to be run on a local computer, while still maintaining enough rows after processing. 

## Procedure to process data set 

To map the original Motor Collisions data set into the Integrated Dataset (processed_motor_collisions.csv), the following steps were performed. 

1. Read the csv file in as a dataframe using pandas
2. Extract the Year from the COLLISION_DATE field into its own column (YEAR) and keep only the collisions that occurred in 2020 
3. Extract the Hour from the COLLISION_TIME field into its own column (hour)
4. Drop the following columns: 
     - UNIQUE_ID
     - COLLISION_ID
     - PERSON_ID
     - PERSON_INJURY
     - PED_ACTION
     - PED_LOCATION 
     - VEHICLE_ID
     - CONTRIBUTING_FACTOR_2
     - CONTRIBUTING_FACTOR_1
     - COLLISION_TIME
     - COLLISION_DATE
     - YEAR
5. Delete rows where the PERSON_AGE value is not between 1 and 100. 
6. Reconcile the PERSON_TYPE and PED_ROLE fields by changing the PED_ROLE to 'Bicyclist' (from 'Driver') when the PERSON_TYPE is 'Bicyclist'. 
7. Drop the rows where PERSON_TYPE is 'Bicyclist' and the PED_ROLE is 'Passenger' (There should be 8 of them)
8. Drop the column PERSON_TYPE as its remaining meaningful values ('Pedestrian', 'Occupant') are represented by the 'PED_ROLE' column, as either 'Driver', 'Bicyclist', 'Pedestrian'
9. Delete rows with null values or 'Unknown' values 
10. Delete rows with 'Does Not Apply', 'Other', '-', 'U' in any of the columns 
11. Discretize Age into bins (0-10, 0-20, 20-30, 30-40, 40-50, 50-60, 60-75, 75-100)
12. Label the values in the dataframe by their column name, for example if the value of a cell in the PERSON_SEX column is F, it becomes PERSON_SEX: F


## Internal Project Design 

A clear description of the internal design of your project; in particular, if you decided to implement variations of the original a-priori algorithm (see above), you must explain precisely what variations you have implemented and why.

## Example run
The command line specification of a compelling sample run (i.e., a min_sup, min_conf combination that produces association rules that are revealing, surprising, useful, or helpful; see above). Briefly explain why the results are indeed compelling.

## Additional Info: 
Any additional information that you consider significant.