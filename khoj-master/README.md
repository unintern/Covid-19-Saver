<H1>KHOJ</H1>

<h3>Steps for creating superuser</h3>

Run following command in your terminal<br>
<code>python manage.py createsuperuser</code>
<br>
Now open django shell and run the following commands<br>
<code>python manage.py shell</code>

Now add following commands in shell<br>
<code>from django.contrib.auth.models import User</code>

Now get the object of the following user<br>
<code>user = User.objects.all()[0]</code><br>
The above command would return 1st user present in the database<br>

Now do the following operations on the objects
<code>user.is_staff = True</code><br>
<code>user.is_verified = True</code><br>
<code>user.is_verified = True</code><br>
<code>user.is_active = True</code><br>
<code>user.save()</code><br>
Exit the terminal<br>
<code>exit()</code><br>

Now the superuser has been created succesfully
