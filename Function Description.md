refresh_data()
- This function loads all the data required to display the home page from file system

getnewTaskID()
- This function is used to generate a new unique TaskID. All our TaskIDs are alphanumeric strings of length 5. Eg. “AAAA2”, “2342V”. No special characters are used for obtaining TaskIDs
- This function randomly produces a possible TaskID and checks if it is already in use. If the generated TaskID is in use, then we keep on generating random TaskIDs until we find one that is not in use.


