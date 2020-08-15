#######################################################
# create or use a client-side cookie storing user name;
# there is no input form data to parse in this example
#######################################################
     
import Cookie, os
cookstr  = os.environ.get("HTTP_COOKIE")
cookies  = Cookie.SimpleCookie(cookstr)
usercook = cookies.get("user")                     # fetch if sent

if usercook == None:                               # create first time 
    cookies = Cookie.SimpleCookie()                # print Set-cookie hdr
    cookies['user']  = 'Brian'
    print cookies
    greeting = '<p>His name shall be... %s</p>' % cookies['user']
else:
    greeting = '<p>Welcome back, %s</p>' % usercook.value 

print "Content-type: text/html\n"                  # plus blank line now
print greeting
