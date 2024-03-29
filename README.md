# Talvido API


1. clone the project using 
```console
git remote add origin https://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@github.com/errajendra/keedsreel.git
```

2. Install all the dependies using this command
```console
pip install -r requirements.txt
```

3. create ```.env``` file, where manage.py file is located and add this code.
```
DATABASE_NAME=talvido
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=12345
DATABASE_HOST=localhost
DATABASE_POST=5432
FIREBASE_API_KEY=AIzaSyAUeupZ8K8k465FgMPLsHBnnSGQoG-2p10

RAZORPAY_KEY_ID=rzp_test_WSpHIcbcEUaGsR
RAZORPAY_KEY_SECRET=OVNdEwmls1o4xjKDqA8LzHdf

ENCRYPTION_KEY=6bf164ba2e842481ef4044276c480aa2

IMAGEKIT_PUBLIC_KEY=public_+l7BlLFOY8X32v/Xu7C/ANro9G8=
IMAGEKIT_PRIVATE_KEY=private_lRFajU5FJIaktO9FtRAou2cNErU=
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/qsximwlqb

# ENCRYPTION_KEY=6bf164ba2e842481ef4044276c480aa2339e664e47be1da70522c95e25eedbd3
```
change your database credentials with mine.

4. open pgadmin4 and create a database called ```talvido```
