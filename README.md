# Guide how to use
This script used to generate different type of 'đơn thuốc'

## I. Run code
There are 3 types of form can be used. To generate data, go to __src folder__ and type following comandline:
> python hoadon_gen.py

The results should be saved in __/data/results__ folder with following structure file name:
> <type_of_distort> _ index _ <type_of_algorithm>.png
## II. Implement
There are 3 ways to implement:
### 1. Vocabulary of contents
Go to __data folder__ and define more contents for each field like: durg, hospital_location, ...

### 2. Form of 'hóa đơn'
Go to __hoadon_gen.py__ in __src folder__, there are 3 functions related to 3 types of form

### 3. Variables of distortion functions
Go to __src folder__, there are 5 types of distortion you can use during generating