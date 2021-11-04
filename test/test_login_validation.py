inp = {"name": "user1", "email": "user1@gmail.com", "emailChoose": "user1@gmail.com"}
        response = requests.post("http://127.0.0.1:5000/update_user_info", data=inp)
