-- Optional demo data for local testing/demo.
-- Run AFTER schema.sql. Passwords below are the bcrypt/werkzeug hash for "password123".
-- (Generate your own with werkzeug.security.generate_password_hash if you prefer.)

INSERT INTO users (name, email, password_hash, bio) VALUES
('Asha Rao', 'asha@example.com', 'scrypt:32768:8:1$PLACEHOLDER_HASH_ASHA', 'Loves hiking and coffee.'),
('Vikram Shah', 'vikram@example.com', 'scrypt:32768:8:1$PLACEHOLDER_HASH_VIKRAM', 'CS student, always up for a walk.'),
('Neha Kulkarni', 'neha@example.com', 'scrypt:32768:8:1$PLACEHOLDER_HASH_NEHA', 'Photography enthusiast.');

-- NOTE: The password hashes above are placeholders and will NOT work for login.
-- To seed real, working demo accounts, register them through the app's
-- /register page instead -- this file is provided only as an optional
-- starting point for inserting sample friendships/notifications once you
-- have real user IDs from the `users` table.

-- Example (replace ids with real ones from your `users` table after registering):
-- INSERT INTO friendships (sender_id, receiver_id, status) VALUES (1, 2, 'accepted');
-- INSERT INTO notifications (user_id, type, message) VALUES (2, 'friend_accepted', 'Your friend request was accepted');
