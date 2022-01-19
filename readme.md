## DESCRIPTION:

Mindful Moments is a meditation and mood-tracking app that helps users increase their mindfulness and prioritize self-care by maintaining accountability and increasing self-reflection. Once registered, users have access to a curated meditation catalog and personal journal to record daily mood check-ins and observations on their meditation sessions. User data input is displayed in the form of a mood graph for a yearly overview of their well-being. The dates displayed in the chart can be used as guidance to search and explore previously logged reflections enhancing self-connection. Text reminders can be scheduled to maintain consistency and reinforce positive habit building while meditations can be favorited for convenience and accessibility.

## TECH STACK:

Python, Flask, SQLAlchemy, PostgreSQL, RegEx, Jinja, Javascript, AJAX, JSON, Bootstrap, HTML, CSS
APIs: Spotify Web API, Twilio

## FEATURES:

- Users can create an account where they can log in and out
- A random inspirational quote and suggested meditation are received after login
- The curated meditation catalog includes track name, track artist, track images (which can be hovered over for a 30 second track preview), and a link to the track url to play audio
- Meditation tracks can be added to favorites or removed for easy accessibility
- Meditations can be searched by track name and artist name
- Random mindfulness tips display on meditation details page when the "Explore" button is clicked
- Journal entries can be submitted to the database
- A mood chart displays a yearly overview of a user's journal submission
- Journal entries are searchable by date (The mood chart can be used as a reference)
- Reminders can be scheduled and deleted
- All reminders can be viewed in chronological order
- Past reminders are automatically removed from the database for user's convenience
- Automated text messages are sent based on a user's scheduled reminders
