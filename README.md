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
To find large itemsets in the dataset, we implemented the a-priori algorithm described in Section 2.1 of Agrawal and Srikant, 1994. The main part of the algorithm is implemented in <code>large-k-itemsets()</code>, which takes a list of items in the dataset, min_sup, and the table itself. It first calls <code>one_itemsets()</code>, which returns L_1, a dictionary of 1-large itemsets and their counts. Then, while the set of k-1-large-itemsets  is not empty, <code>apriori_gen()</code> returns C_k, the set of candidate k-large-itemsets. We iterate through the table's rows to check how many rows each candidate itemset appears in, and check if the itemset's support is at least min_sup. If so, then that itemset is added a set of new k-large itemsets. <code>large-k-itemsets()</code> returns a dictionary of all large-itemsets and their counts.

We implemented <code>aprior_gen()</code> as described in Agrawal and Srikant, 1994, using their join and prune algorithm.

To find the high confidence association rules, we generate possible association rules for each large itemset and calculate confidence with <code>count(LHS,RHS)/count(LHS)</code> using the large-itemsets dictionary. If the confidence is at least min_conf, then that rule is added to the set of high confidence associaton rules. This is implemented in <code>compute_confidence()</code>.


## Example run
<code>python3 association_rules.py processed_motor_collisions .5 .6</code>
min_sup = .5 and min_conf = .6 seems to result in the most appropriate amount of meaningful association rules.

Some interesting rules include:
['EMOTIONAL_STATUS: Conscious'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 67.98%, Supp: 96.4%)
['EJECTION: Not Ejected'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 70.63%, Supp: 95.2%)
['EJECTION: Not Ejected', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EMOTIONAL_STATUS: Conscious] (Conf: 97.21%, Supp: 67.2%)
['POSITION_IN_VEHICLE: Driver'] => [EJECTION: Not Ejected] (Conf: 93.39%, Supp: 65.7%)

We can see that 67% of the time when the participant was conscious, there was a lab belt and harness, thus suggesting seatbelt's safety importance. Similarly, 70.63% of the time when the participant was not ejected from the vehicle, he or she was wearing a seatbelt. Also, when the participant was not ejected and wearing a seatbelt, 97% of the time the participant was conscious. Therefore, from these rules we can hypothesize that seatbelts do protect participants from severe outcomes in accidents.

If we lower the min_sup and min_conf thresholds to allow for more rules, we can see even more revealing association rules associated with safety. Although lower min_sup and min_conf result lots of rules that might not be meaningful, there are still plenty that we extract information from. 

For example (from min_sup=.15 and min_conf=.55):
['PERSON_SEX: M'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 62.13%, Supp: 57.5%)
['PERSON_SEX: F'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 74.60%, Supp: 42.5%)
['AGE_RANGE: (30, 40]'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 68.14%, Supp: 23.5%)
['AGE_RANGE: (20, 30]'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 65.16%, Supp: 27.1%)
['SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EJECTION: Not Ejected] (Conf: 99.71%, Supp: 67.4%)
['POSITION_IN_VEHICLE: Driver'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 66.47%, Supp: 65.7%)
['AGE_RANGE: (20, 30]', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EMOTIONAL_STATUS: Conscious] (Conf: 97.10%, Supp: 17.7%)
['PERSON_SEX: F', 'POSITION_IN_VEHICLE: Driver'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 77.05%, Supp: 22.2%)
['PED_ROLE: Passenger', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EJECTION: Not Ejected] (Conf: 99.78%, Supp: 23.9%)
['PED_ROLE: Driver', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EMOTIONAL_STATUS: Conscious] (Conf: 96.94%, Supp: 43.4%)

Some of these relations show some shocking statistics about seatbelt usage in accidents:
  Only 62% of men in these accidents were lab belts and harnesses, while 75% of women did.
  Only 68% and 65% of people in their 30s and 20s, respectively, wore seatbelts.
  77% of female drivers wore seatbelts.
  Only 66% of drivers wore seatbelts.

Seatbelts are also shown to be effective in preventing severe injury:
  Nearly 100% of the time wearing seat belts led to not being ejected.
  97% of participants who are in their 20s and are wearing seatbelts will be conscious.
  Nearly 100% of passengers who wore seatbelts were not ejected.
  97% of drivers who wore seatbelts were not ejected.

## Additional Info:
Any additional information that you consider significant.
