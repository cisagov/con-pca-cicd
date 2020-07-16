db.createUser(
    {
        user: "root",
        pwd: "rootpassword",
        roles:[
            {
                role: "readWrite",
                db:   "pca_data_dev"
            }
        ]
    }
);