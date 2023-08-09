INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name="Rock Playlist"), (SELECT songId FROM songs WHERE title="Learn to Fly"));
INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name="Rock Playlist"), (SELECT songId FROM songs WHERE title="Friday I'm In Love"));
INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name="Rock Playlist"), (SELECT songId FROM songs WHERE title="This Charming Man"));
INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name="Rock Playlist"), (SELECT songId FROM songs WHERE title="Battle of Evermore"));
INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name="Rock Playlist"), (SELECT songId FROM songs WHERE title="Born to Run"));
INSERT INTO playlists_to_songs (playlistId, songId) VALUES ((SELECT playlistId FROM playlists WHERE name="Rock Playlist"), (SELECT songId FROM songs WHERE title="Badlands"));

