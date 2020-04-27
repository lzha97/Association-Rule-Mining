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
2. Extract the Year from the `COLLISION_DATE` field into its own column (`YEAR`) and keep only the collisions that occurred in 2020
3. Extract the Hour from the `COLLISION_TIME` field into its own column (`hour`)
4. Drop the following columns:
     - `UNIQUE_ID`
     - `COLLISION_ID`
     - `PERSON_ID`
     - `PERSON_INJURY`
     - `PED_ACTION`
     - `PED_LOCATION`
     - `VEHICLE_ID`
     - `CONTRIBUTING_FACTOR_2`
     - `CONTRIBUTING_FACTOR_1`
     - `COLLISION_TIME`
     - `COLLISION_DATE`
     - `YEAR`
5. Delete rows where the `PERSON_AGE` value is not between 1 and 100.
6. Reconcile the `PERSON_TYPE` and `PED_ROLE` fields by changing the `PED_ROLE` to 'Bicyclist' (from 'Driver') when the `PERSON_TYPE` is 'Bicyclist'.
7. Drop the rows where `PERSON_TYPE` is 'Bicyclist' and the `PED_ROLE` is 'Passenger' (There should be 8 of them)
8. Drop the column `PERSON_TYPE` as its remaining meaningful values ('Pedestrian', 'Occupant') are represented by the `PED_ROLE` column, as either 'Driver', 'Bicyclist', 'Pedestrian'
9. Delete rows with null values or 'Unknown' values
10. Delete rows with 'Does Not Apply', 'Other', '-', 'U' in any of the columns
11. Discretize `PERSON_AGE` into bins (0-10, 0-20, 20-30, 30-40, 40-50, 50-60, 60-75, 75-100) in a new column `AGE_RANGE`
12. Label the values in the dataframe by their column name, for example if the value of a cell in the `PERSON_SEX` column is 'F', it becomes 'PERSON_SEX: F'


## Internal Project Design
To find large itemsets in the dataset, we implemented the a-priori algorithm described in Section 2.1 of Agrawal and Srikant, 1994. The main part of the algorithm is implemented in <code>large-k-itemsets()</code>, which takes a list of items in the dataset, min_sup, and the table itself. It first calls <code>one_itemsets()</code>, which returns L_1, a dictionary of 1-large itemsets and their counts. Then, while the set of k-1-large-itemsets  is not empty, <code>apriori_gen()</code> returns C_k, the set of candidate k-large-itemsets. We iterate through the table's rows to check how many rows each candidate itemset appears in, and check if the itemset's support is at least min_sup. If so, then that itemset is added a set of new k-large itemsets. <code>large-k-itemsets()</code> returns a dictionary of all large-itemsets and their counts.

We implemented <code>aprior_gen()</code> as described in Agrawal and Srikant, 1994, using their join and prune algorithm.

To find the high confidence association rules, we generate possible association rules for each large itemset and calculate confidence with <code>count(LHS,RHS)/count(LHS)</code> using the large-itemsets dictionary. If the confidence is at least min_conf, then that rule is added to the set of high confidence associaton rules. This is implemented in <code>compute_confidence()</code>.


## Example run
<code>python3 association_rules.py processed_motor_collisions .5 .6</code>
<br> 
`min_sup` = .5 and `min_conf` = .6 seems to result in the most appropriate amount of meaningful association rules.

Some interesting rules include:
- ['EMOTIONAL_STATUS: Conscious'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 67.98%, Supp: 96.4%)
- ['EJECTION: Not Ejected'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 70.63%, Supp: 95.2%)
- ['EJECTION: Not Ejected', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EMOTIONAL_STATUS: Conscious] (Conf: 97.21%, Supp: 67.2%)
- ['POSITION_IN_VEHICLE: Driver'] => [EJECTION: Not Ejected] (Conf: 93.39%, Supp: 65.7%)

We can see that 67% of the time when the person was conscious, there was a lab belt and harness, thus suggesting seatbelt's safety importance. Similarly, 70.63% of the time when the participant was not ejected from the vehicle, he or she was wearing a seatbelt. Also, when the participant was not ejected and wearing a seatbelt, 97% of the time the participant was conscious. Therefore, from these rules we can hypothesize that seatbelts do protect participants from severe outcomes in accidents.

If we lower the `min_sup` and `min_conf` thresholds to allow for more rules, we can see even more revealing association rules associated with safety. Although lower `min_sup` and `min_conf` result in lots of rules that might not all be equally meaningful, there are still plenty that we can extract relevant information from. 

For example (from min_sup=.15 and min_conf=.55):
- ['PERSON_SEX: M'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 62.13%, Supp: 57.5%)
- ['PERSON_SEX: F'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 74.60%, Supp: 42.5%)
- ['AGE_RANGE: (30, 40]'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 68.14%, Supp: 23.5%)
- ['AGE_RANGE: (20, 30]'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 65.16%, Supp: 27.1%)
- ['SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EJECTION: Not Ejected] (Conf: 99.71%, Supp: 67.4%)
- ['POSITION_IN_VEHICLE: Driver'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 66.47%, Supp: 65.7%)
- ['AGE_RANGE: (20, 30]', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EMOTIONAL_STATUS: Conscious] (Conf: 97.10%, Supp: 17.7%)
- ['PERSON_SEX: F', 'POSITION_IN_VEHICLE: Driver'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 77.05%, Supp: 22.2%)
- ['PED_ROLE: Passenger', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EJECTION: Not Ejected] (Conf: 99.78%, Supp: 23.9%)
- ['PED_ROLE: Driver', 'SAFETY_EQUIPMENT: Lap Belt & Harness'] => [EMOTIONAL_STATUS: Conscious] (Conf: 96.94%, Supp: 43.4%)
- ['PERSON_SEX: M', 'POSITION_IN_VEHICLE: Driver'] => [SAFETY_EQUIPMENT: Lap Belt & Harness] (Conf: 61.06%, Supp: 43.5%)

Some of these relations show some shocking statistics about seatbelt usage in accidents:
  - Only 62% of men in these accidents wore lab belts and harnesses, while 75% of women did.
  - Only 68% and 65% of people in their 30s and 20s, respectively, wore seatbelts.
  - 77% of female drivers wore seatbelts.
  - Only 61% of male drivers wear seatbelts.
  - Only 66% of drivers wore seatbelts.

Seatbelts are also shown to be effective in preventing severe injury:
  - Nearly 100% of the time wearing seat belts led to not being ejected.
  - 97% of participants who are in their 20s and are wearing seatbelts will be conscious.
  - Nearly 100% of passengers who wore seatbelts were not ejected.
  - 97% of drivers who wore seatbelts were not ejected.

Even lower `min_sup` values may result in more interesting rules. 

## Additional Info:

Sample output for combinations of every 0.05 increment of `min_sup` and `min_conf` are included in the "colab output" folder of [this repo](https://github.com/lzha97/Association-Rule-Mining). The summary of these sample runs can be found in the file "colab-results.txt" in the same repo. These outputs were obtained by running the algorithm for possible 0.05 increment combinations of `min_sup` and `min_conf` in a colaboratory notebook. 


We also found that a lower `min_sup` resulted in some meaningful rules that are not returned by runs with higher `min_sup` parameters. This may be because the dataset is skewed so that some columns predominantly feature one value, and include only a tiny fraction of non-dominant values. For example, some distributions are shown below. 


### `PERSON_SEX`

Only around 42% of collisions involved females so `min_sup` needs to be below 42% in order to see rules relevant to `F` or females.
![PERSON_SEX](https://lh3.googleusercontent.com/8Ax7fq7C9LQngvNOUotncYn931JrGiqpUPwt04uc4J59reYj6IzFo95gRbv4tSrNCgkdmitvUNc9DCt-Lo890pF9DuvH1cYC4HzUis3HejNk2fBw_3RgZ-y2phuYF13aVLkNFAlnUR81WoiJAbxPpYGb8o3W4_xkcAZg33R3a8XCZj4qzG3y3pc0hcBcIpbIh7Nf5FKv4N4XL2KOawOugNMOOZsU0aHehwctHTLKdsoBPSngCbBJeTIeFwtISjq88mgtRmU3FeaSZDIggmEEkqXweMfikqV-aYryCEmmHs9E4nwEUN8dAr580XG4s3X7Ub2SEOmyhR7mikHr48ofpKfmr9k6NbkBmkAt48ondaIMcIT57-jQszIfHQpGBwjcBCYSMwinuNR9NLQ8tMRfWmv77uu5LT8NqfG_obMOKBF_j6lJdFUCPIw62DIydSeo6VN8xYhU0uvNl81lpg0ZnC59qhJ2SqAyOezmDOeu554PH5bwL5-7Q7I-tYB8-1_CzFl1-2HkJd-wMMIOzsqMXTlmv_qStm4hQkC-Io-qB0rKlx0_p3ezf1uzyZ5Xc-6u9oqzp2wamMvm8onJwxkPDmKgKkoDf2iIzAB9zBjHuvI6B28frugo9VDRBZokqcM-VI0-jUfmqeSZGDoWB1n3WEokJ_yJaV2I-cd3vMBnby0n5q-xyjfYyb3lMv1al4K6hbWlmJsZXGrangm0U_6P7FFkmlTE-JMErW6-lhzSkBgzRdLn3tUmNQ=w1002-h320-no)

### `Ejection`

For `min_sup` values that are not very low, only collisions in which the person was 'Not Ejected' will be represented. 

![Ejection](https://lh3.googleusercontent.com/AtGM6ynthN89MVEx4VkVIVfW2MXo2YkBBZOBjalUoKUeHNnBzuZd4k0LrTxLlL02JWkpeu_j5meuoiKlbSd0jn8Ci8SoaXQuJExbOXzpFo5vsXyXDmfEGygzl-JnX61UaKX-ImvGiQyt0YiEEWUvI9FfnmZmtEuV0keVpNe7FOMyTT4MgrcBRSF7CI0Fjzm5URVBI8sR6ir8vP4mfGpSg_GDopxC8E0O2xJhpQG2uRXXcIGJfGeJBZ_kI85eliv3RdOmHgbBFQimHbDFUZkgljcz07YSMRUrgqz3EhexP-xP-iQjBKvKwmwH0rAEdsBrQW8yoteINXjCx5X3GnWN_WdXAP7odqPGbkQEUY92pdtsh1lIZiNH7zuUk8MSkI_dRK7dg6JACMtUfEoB0RM3QK_U88BMXuV36JlpsFMDzBb1OjXwDLdLdh9M2UyyI3a7Lmxps8te-TtPxTVThJaXbeX-eUT0rXbjJPjGufCK51OSfhUjkzPBW0bK2F55UCrW2Aw31Ge0tzEsrWoqHOI5CAx87io3VTMZS9MnwNxaE9mgeWR1sZ7Z8P_-ok75AWO34shBmHPt7TIonMC_trMjtizo8SIavAYCKwqVkiGWhSNgby-j_zCzrVtCcYMmQEuDb9WKByEoNMqkb01A1A5MESMhQpRVaXgrsvXSduOkU4YyanrgYWyiFOivy6Zt-rtYLmpaeSIBq7F20XCiuUHqE6Ct7eKg-cFtgFU9r5dJAo3GiUE_MxV2Cg=w996-h318-no)

### `PED_ROLE`

`min_sup` needs to be very low in order to see rules about pedestrians or bicyclists or in-line skaters.
![PED_ROLE](https://lh3.googleusercontent.com/qT4aAnka2igC0vT2VfEcWXOFUOXs6QCAiZaIJUDCEXdNwwynIA5G3G-a3rSrHJFyh_y4rrUMWcw2fvccgeGNGZZwNZ8tL9xWbKpx-ZbkdwJ0eKRqm4MG8wvDfW9qtDfHERPGCtW9l7gQRz8u2ooH8b6jdI377zNmY6hLMbV5SPlAOI2UZu8Df504C1sqE-HGVTTL3Q3CCtUDN9DNwgDglnVHjEvpdzgaX4dHs-JZ2u3YD_Tcf4KBNrS7BxkfMbs2pGHvUXQnvzJEXMSJ8_7UtutOKrRAah8n2hbHNMLUVaNJ3zvGlgZfuawa4YkJ6OHwUb_4OFeN7DKZvBqXlMZurmiUCFyGXq0Wkht8n5UIe4QcWBcHXrKu01fvZpn9bQNf21OMT_6cCxP3LVxUsfqeNuhMeUqJF96f-71Zy57oDCbY9JP2-YCTO6O7bJO5yqXZ4hBs0v1rRgi1UYTUdm_JTnKj0vTLGOuOM_rFmIQmeGeSax2aPR5jkM-Xt85aemf4HubF8tfWaMAQUkwJtFCkLzgElMNQO227oxuXo2vzPCHAkysSEfefqe04tibIxa9Xte2Bsm4k4MpdsEnCRHgeQblzLeGMdbC4jZj-Tazv5epEUr1aXTmdVfaphoNt5jEjsQj94oWVUASrQ2uAEjCybUNDbJFpkeHgk8fRvqolOEx3D9fgupuSaSZiKR3cUOMtlAhSMniU64Z9BNXBVCQLILjtmYqxpc7g52HrWMZscj20RmE2ABHxQQ=w998-h324-no)


### `EMOTIONAL_STATE`
Thankfully, most people emerged 'Conscious' from motor collisions, however to generate rules showing what sort of conditions resulted in more serious states, the `min_sup` parameter needs to be sufficiently low, as these states only make up a tiny fraction of the ~7000 rows of the Integrated Dataset.
![EMOTIONAL_STATE](https://lh3.googleusercontent.com/HkNZGAFibBVidS4onH74DIAs55CMbj9kCogYTCtuUsaOh7O3HlsVYFErdU-y3YWE2piBsQJhp9oJ5qg_B1fNVMXBrQEcHDS3afDcSJXXkHVZQNQh2zoiP5v5CYw7pz-vtANHKuy1mGjog2hw3_Jv1uqRmE8u4iSpm4fsL9_sdGWUgeLgr8QS-9Db3nfJ5TLDio4SEvJX3VcEsw_pgCBDe6Wx-bukZfWfirffvj9n7wrtL_WdcUpalpeMnJCep47YIaogcDM8DtuP9YOyfL3gb7afTLv_iY09er8PfAFKiafIrnZT6jq0j8u-As1M4HgM0xbD08sCutL7EL3qjo6SvZLhN-IFrxHXzioeAbqXQMU8h6Uj5IJAf1Go03eP9dzBtF-ldeg6uWV2GXX7TQmpw45zWiwaGmO9fp9C31R6fH08LJMt8O5TXGJK8onhHlwfOq0Lu_V9mzt-dT5DxpJSA3A2He3rPNePzMoJWwGa1Km1O4ze4jX0WgRSSyugVc5NjQgej57DhuG8Cavr5jJYd7UbbPafwW12HJsoYayf-zIMzet46D1dhi-ULlIeRBH42dhP7eSYdEeUur4zlsmcNsjE-bOEwlx_E0yNCuM13TaNzluw-wYfyRhX7AUi-5wo4UH80Af-swU5H-7Nn8r_7ChK5lZeEQDr_tS4Mf5vWHyy3AJ6MVtWbH_85GqU8aE-9puDqq7c1liwFj--WWdkRpsL-hmGqeY_w8bNX94v05JYMqimieco3A=w1014-h324-no)
