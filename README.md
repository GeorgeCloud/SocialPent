# SocialPent

Description:


TODO
  1-2 point
  - [ ] Add 'bio' column to user model,
    - [ ] Allow users to add a bio in their profile
  - [ ] Add 'coordinates' column to post model
    - [ ] When a user posts save their coordinates using HTML5 geolocation to the post data
  - [ ] Create edit/delete route for posts

  3 point
  - [ ] Create Event Table
    - [ ] When requesting data from API save it into database

  4+ points
  - [ ] Normalize Event Data Coordinates and user's coordinates (This will bring down our number of API requests - max 5000 API calls per day)
  - [ ] Track words within event data by creating a table; Trending words(24hrs)
  - [ ] Implement backend workers to handle online/offline user status
  - [ ] Add notifications, background worker
