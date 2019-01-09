# iTunesMessageExtract
Extracts SMS and iMessages for a given phone number from the most recent local iTunes backup.
- Only works on windows machines where the iTunes backups exist and are in their default location.
- Only works for finding messages to or from a phone number with the '+1' country code.
- Retrieves the date, time, service (iMessage or SMS), if the message was sent or received, and message text for all messages sent to or received from a given phone number.

# To Run
There are a few options to run the program
1. Run as a python script
2. Build Executable using build.bat (requires pyinstaller)
3. Run the dist/iTunesMessageExtract.exe executable file. This executable has no external dependencies and does not require python.
