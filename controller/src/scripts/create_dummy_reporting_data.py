retval = {}
for i in range(1,100):
    retval = { 
        "email": f"Email{i}@test.test",
        "first_name": f"fName-{i}",
        "last_name": f"lName-{i}",
        "position": f"manager"
    }
    print(str(retval) + ",")