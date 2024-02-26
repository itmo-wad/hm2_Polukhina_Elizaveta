
# Homework2

## Description
1. The project implements user authentication in the form via the POST method. Upon successful authorization, the username is recorded in the session and the user profile is displayed. 

When you log out of your account, the session is cleared.

If the input is unsuccessful, the user is prompted to re-enter the authorization data.

If the user is not logged in, they cannot get into the profile, as they are redirected to the authentication page.

Usernames and passwords are stored in MongoDB.

2. The possibility of creating a new user has been created. During registration, it is checked whether a user with such a username exists. If not, then the username entered by the user and the hashed password using the hashlib library.

Then, during authorization, the hash of the entered password and the hash in the database will be compared.

The user's page has his name, photo, city of residence and hobbies. If desired, the user can change the data by entering it into the form via the POST method.

Changing the password works the same way. A request is sent to the server, the hash of the entered old password is compared with the password from the database. In case of a match, the hash of the new password is saved using the update_one directive, indicating the user's nickname and the field to be changed.

The default image is displayed on the user's page. I save the photo uploaded by the user in the uploads folder. Unfortunately, I have not yet been able to get a photo from the uploads folder.




