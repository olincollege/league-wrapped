# League Wrapped
League Wrapped uses the Riot Games API to create Spotify Wrapped style lowlights for players.

## Dependencies
League Wrapped uses the following packages:
- pandas
- pillow/PIL
- requests
- riotwatcher
- tk (tkinter)

These packages are listed in `requirements.txt` and be installed by running the following line in the command prompt:
`pip install -r requirements.txt`

## Creating an API key
To use the Riot Games API, you will need to create an API key. This can be done by following the steps below:

1. Sign in at the [Riot Developer Website](https://developer.riotgames.com/)
2. Generate/Regenerate an API key
3. Create a file called `key.txt` in the root directory
4. Copy the API key into the first line of `key.txt`