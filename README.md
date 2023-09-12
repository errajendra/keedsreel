# Talvido API


1. clone the project using 
```console
git clone https://github.com/dharma-wooshelf/talvido.git
```

2. Install all the dependies using this command
```console
pip install -r requirements.txt
```

3. create ```.env``` file, where manage.py file is located and add this code.
```
DATABASE_NAME=talvido
DATABASE_USERNAME=aashish
DATABASE_PASSWORD=1234
DATABASE_HOST=localhost
DATABASE_POST=5432
FIREBASE_API_KEY=AIzaSyAAFVJZkY2c_5RXCUoqrcuLacXFvsjEshk
RAZORPAY_KEY_ID=rzp_test_WSpHIcbcEUaGsR
RAZORPAY_KEY_SECRET=OVNdEwmls1o4xjKDqA8LzHdf
IMAGEKIT_PUBLIC_KEY=public_8l0oKGRT0x0pzX2xI1xo/X9mGzA=
IMAGEKIT_PRIVATE_KEY=private_sf1ZZcKVxGonl9f85J452dZJY2k=
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/af16umqa5
ENCRYPTION_KEY=6bf164ba2e842481ef4044276c480aa2339e664e47be1da70522c95e25eedbd3
```
change your database credentials with mine.

4. open pgadmin4 and create a database called ```talvido```
