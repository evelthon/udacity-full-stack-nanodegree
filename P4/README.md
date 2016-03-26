# Project 4 - Conference Organization
## About
A cloud based project for conference organization

## Task 1: Add Sessions to a Conference
The required endpoints for sessions and speaker where created. Specifically:
1. The speaker is a property of the Session class. It is a required string.
Alternatively, the speaker could be linked to a user account for this to be
more consistent.
2. Sessions where designed as children of the conference. As such, the ancestor
keyword was used to signify this.
1. The speaker is a property of the Session class. It is a `required string`.
Alternatively, the speaker could be linked to a user account for this to be
more consistent. Still, doing so would require the speaker to register as a
user.
2. Sessions where designed as children of the conference. As such, the ancestor
keyword was used. This allows for sessions to be queried by
their conference ancestor.

## Task 2: Add Sessions to User Wishlist
The Profile model was modified to add a `sessionWishlist` property. This
property is used to store unique session keys for each user and is use by the
three endpoint methods created for this task, `addSessionToWishlist`,
`getSessionsInWishlist`, `deleteSessionInWishlist`.

## Task 3: Work on indexes and queries
For this task the requirement was to create 2 additional queries. For this
reason the following endpoint methods where created:
1. `getFutureSessions`: List all future sessions remaining since now.
2. `getPreConferenceSessions`: List pre-conference sessions, that's sessions
occuring before the main conference starts.

Additionally we need to query for non-workshop sessions occuring before 19:00
The problem here is that ndb queries in app engine support multiple inequality
filter as long as they are on the same property. This is not the case here.

A solution to this would be to use ndb/app engine to filter by one property,
then filter that data by the second property natively in python.

## Task 4: Add a Task

For this task the requirement was to create 2 additional queries. For this
reason the following endpoint methods where created:
1. `getFutureSessions`: List all future sessions remaining since now.
2. `getPreConferenceSessions`: List pre-conference sessions, that's sessions
occuring before the main conference starts.

Additionally we need to solve a query problem for non-workshop sessions
occuring before 19:00. The problem here is that ndb queries in app engine
support multiple inequality filter as long as they are on the same property.
This is not the case here.
A solution to this would be to use ndb/app engine to filter by one property,
then filter that data by the second property natively in python.

## Task 4: Add a Task
This task required the creation of a new endpoint method called
`getFeaturedSpeaker`. This method would get the featured speaker if one exists
from memcache. For this to happen, `_createSessionObject` was modified to save
in memcache a speaker with many sessions.

## Setup Instructions
1. Download and install the [Google App Engine SDK][1] for Python
2.. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
3. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][2].
4. (Optional)Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
5. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
6. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
7. (Optional) Generate your client library(ies) with [the endpoints tool][3].
8. Deploy your application.

[1]: https://cloud.google.com/appengine/downloads
[2]: https://console.developers.google.com/
[3]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool

