---BETTY MOVIE DATABASE (BMDB) ---

My first app - a quick tool for randomly choosing 3 films from a preset list based on a selected category in order to help you decide what to watch tonight. 

Users can also search for a new film to add to the database by title, pulling through the film's release poster, release date and synopsis from The Movie Database API (https://developer.themoviedb.org/docs/getting-started)

During the building and deployment of this app has allowed I have been using the following:

- Flask
- Jinja
- HTML
- CSS
- Bootstrap
- PostgreSQL
- APIs

---------RELEASE NOTES---------

v1.1 
New features added:
 - filter bar added to Film List page to search for films in database by title
 - New admin authentication added - anyone can use the random film selector but the ability to add, edit or delete films is now restricted to admins
 - New admins can be registered by an existing admin only. Unauthorised visits to the /register endpoint are blocked
 - Improved error handling and user feedback via flash messaging

v1.0
Initial release at basic app

