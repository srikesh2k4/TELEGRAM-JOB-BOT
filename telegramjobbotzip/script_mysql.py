import configparser
from telethon import TelegramClient, events
from datetime import datetime
import mysql.connector

# Initializing Configuration
print("Initializing configuration...")
config = configparser.ConfigParser()
config.read('config.ini')

# Read values for Telethon and set session name
API_ID = config.get('default', 'api_id')
API_HASH = config.get('default', 'api_hash')
BOT_TOKEN = config.get('default', 'bot_token')
session_name = "sessions/Bot"

# Read values for MySQLdb
HOSTNAME = config.get('default', 'hostname')
USERNAME = config.get('default', 'username')
PASSWORD = config.get('default', 'password')
DATABASE = config.get('default', 'database')

# Start the Client (telethon)
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize MySQL connection
conn = mysql.connector.connect(
    host=HOSTNAME,
    user=USERNAME,
    password=PASSWORD,
    database=DATABASE
)

# Create a cursor object using the connection
crsr = conn.cursor()

# Function to create tables if they don't exist
def create_tables():
    try:
        # Create table for event registration
        crsr.execute("""
            CREATE TABLE IF NOT EXISTS event_reg (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(15),
                email VARCHAR(255),
                event_name VARCHAR(255),
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create table for complaint registration
        crsr.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(15),
                email VARCHAR(255),
                description TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create table for callback registration
        crsr.execute("""
            CREATE TABLE IF NOT EXISTS callback_reg (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(15),
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")

# Function to insert event registration into database
def insert_event_registration(name, phone, email, event_name):
    try:
        sql_command = """
            INSERT INTO event_reg (name, phone, email, event_name) 
            VALUES (%s, %s, %s, %s)
        """
        crsr.execute(sql_command, (name, phone, email, event_name))
        conn.commit()
    except Exception as e:
        print(f"Error inserting event registration: {e}")

# Function to insert complaint into database
def insert_complaint(name, phone, email, description):
    try:
        sql_command = """
            INSERT INTO complaints (name, phone, email, description) 
            VALUES (%s, %s, %s, %s)
        """
        crsr.execute(sql_command, (name, phone, email, description))
        conn.commit()
    except Exception as e:
        print(f"Error inserting complaint: {e}")

# Function to insert callback registration into database
def insert_callback_registration(name, phone):
    try:
        sql_command = """
            INSERT INTO callback_reg (name, phone) 
            VALUES (%s, %s)
        """
        crsr.execute(sql_command, (name, phone))
        conn.commit()
    except Exception as e:
        print(f"Error inserting callback registration: {e}")

# Command for event registration
@client.on(events.NewMessage(pattern="(?i)/event_reg"))
async def event_register(event):
    try:
        # Parse user input and insert into 'event_reg' table
        data = event.message.text.split(" ")[1:]  # Skip the command itself
        if len(data) == 4:
            insert_event_registration(*data)
            await event.reply("Event registration successful!")
        else:
            await event.reply("Invalid format. Use: /event_reg <name> <phone> <email> <event_name>")
    except Exception as e:
        await event.reply("Error processing your request.")

# Command for complaint registration
@client.on(events.NewMessage(pattern="(?i)/complaint"))
async def complaint_register(event):
    try:
        # Parse user input and insert into 'complaints' table
        data = event.message.text.split(" ")[1:]  # Skip the command itself
        if len(data) >= 4:
            description = " ".join(data[3:])
            insert_complaint(data[0], data[1], data[2], description)
            await event.reply("Complaint registration successful!")
        else:
            await event.reply("Invalid format. Use: /complaint <name> <phone> <email> <description>")
    except Exception as e:
        await event.reply("Error processing your request.")

# Command for callback registration
@client.on(events.NewMessage(pattern="(?i)/callback"))
async def callback(event):
    try:
        # Parse user input and insert into 'callback_reg' table
        data = event.message.text.split(" ")[1:]  # Skip the command itself
        if len(data) == 2:
            insert_callback_registration(*data)
            await event.reply("Callback registration successful!")
        else:
            await event.reply("Invalid format. Use: /callback <name> <phone>")
    except Exception as e:
        await event.reply("Error processing your request.")

# Command for /start
@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """👋 Welcome to SRM Job Bot!

I am thrilled to assist you in your job search journey. Here are the options available:

1. 🌟 /explore - Explore Job Openings
2. 📅 /events - Stay Updated on Events
3. ℹ️ /about - Learn About SRM
4. ❓ /questions - Ask Questions
5. 🆘 /help - Get Help
6. 📝 /track - Application Tracking
7. 📞 /contact - Contact Us
8. 📋 /register - Register for Job
9. 💼 /event_reg - Register for Events
10. ⚠️ /complaint - Register a Complaint
11. 🔄 /callback - Request a Callback

Type the corresponding command to access the feature you're interested in. Let's find the perfect opportunity for you at SRM!
"""
    await client.send_message(SENDER, text)

# Command for /explore
@client.on(events.NewMessage(pattern="(?i)/explore"))
async def explore(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # Sample job list
    job_list = """
    🌟 **Current Job Openings**

    1. Software Engineer - Full Stack Developer
    2. Marketing Specialist
    3. Research Assistant - Computer Science
    4. HR Coordinator
    5. Financial Analyst
    """

    # set text and send message
    text = f"""🌟 **Explore Job Openings**

To explore the latest job openings at SRM, visit our careers page [here](careers_link).

{job_list}

You'll find a wide range of exciting opportunities waiting for you. Let's discover the perfect role for your skills and aspirations!
"""
    await client.send_message(SENDER, text)

# Command for /events
@client.on(events.NewMessage(pattern="(?i)/events"))
async def event(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # Sample event list
    event_list = """
    📅 **Upcoming Events**

    1. Job Fair - May 15, 2024
    2. Industry Panel Discussion - June 5, 2024
    3. Networking Mixer - June 20, 2024
    4. Career Development Workshop - July 10, 2024
    5. Tech Talk Series - July 25, 2024
    """

    # set text and send message
    text = f"""📅 **Stay Updated on Events**

To stay informed about upcoming events at SRM, keep an eye on our events calendar [here](events_link).

{event_list}

From job fairs to networking sessions, there's always something happening. Don't miss out on valuable opportunities – mark your calendar today!
"""
    await client.send_message(SENDER, text)

# Command for /about
@client.on(events.NewMessage(pattern="(?i)/about"))
async def about(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """ℹ️ **Learn About SRM University**

SRM University is a prestigious institution known for its commitment to excellence in education and research. With state-of-the-art facilities and a diverse community of students and faculty, SRM offers a vibrant learning environment.

To learn more about SRM's history, vision, and mission, visit our website [here](srm_website_link).

Join us in shaping the future through education and innovation!
"""
    await client.send_message(SENDER, text)

# Command for /questions
@client.on(events.NewMessage(pattern="(?i)/questions"))
async def questions(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """❓ **Ask Questions**

Have any questions about SRM or our job opportunities? Feel free to reach out to us!

You can contact our support team via email at support@srm.com or through our contact form [here](contact_form_link).

We're here to help you every step of the way!
"""
    await client.send_message(SENDER, text)

# Command for /help
@client.on(events.NewMessage(pattern="(?i)/help"))
async def help(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """🆘 **Get Help**

Need assistance or guidance? Our support team is here for you!

You can reach out to us via email at help@srm.com or through our contact form [here](contact_form_link).

Don't hesitate to ask – we're committed to ensuring your success!
"""
    await client.send_message(SENDER, text)

# Command for /track
@client.on(events.NewMessage(pattern="(?i)/track"))
async def track(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """📝 **Application Tracking**

Track the status of your job applications with ease!

Log in to your candidate portal [here](candidate_portal_link) to view updates, schedule interviews, and more.

Your journey with SRM starts here – stay informed and engaged!
"""
    await client.send_message(SENDER, text)

# Command for /contact
@client.on(events.NewMessage(pattern="(?i)/contact"))
async def contact(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """📞 **Contact Us**

Have inquiries or need assistance? We're just a message away!

You can reach out to us via email at contact@srm.com or through our contact form [here](contact_form_link).

We're here to support you throughout your journey!
"""
    await client.send_message(SENDER, text)

# Command for /register
@client.on(events.NewMessage(pattern="(?i)/register"))
async def register(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id

    # set text and send message
    text = """📋 **Register for Job**

To register for job opportunities at SRM, please provide the following information:

**Format:** /reg <name> <phone_number> <email> <department> <position_selected_to_join>

- `<name>`: Your full name.
- `<phone_number>`: Your phone number (up to 15 digits).
- `<email>`: Your email address.
- `<department>`: The department you're interested in.
- `<position_selected_to_join>`: The position you're interested in joining.

For example:
/reg John_Doe 1234567890 johndoe@example.com Engineering_Software_Engineer

Once you've completed the form, you'll be considered for relevant job openings. Let's kickstart your career journey with SRM!
"""
    await client.send_message(SENDER, text)

# Command for /select
@client.on(events.NewMessage(pattern="(?i)/select"))
async def select(event):
    try:
        # Get the sender of the message
        sender = await event.get_sender()
        SENDER = sender.id

        # Execute the query and get all (*) the registrations
        crsr.execute("SELECT * FROM reg")
        res = crsr.fetchall()  # fetch all the results

        # If there is at least 1 row selected, print a message with the list of all the registrations
        if res:
            text = create_message_select_query(res)
            await client.send_message(SENDER, text, parse_mode='html')
        # Otherwise, print a default text
        else:
            text = "No registrations found inside the database."
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e:
        print(e)
        await client.send_message(SENDER, "Something went wrong... Check your code!", parse_mode='html')
        return

# Command for /delete
@client.on(events.NewMessage(pattern="(?i)/delete"))
async def delete(event):
    try:
        # Get the sender
        sender = await event.get_sender()
        SENDER = sender.id

        # Get the text of the user AFTER the /delete command and convert it to a list (we are splitting by the SPACE " " symbol)
        list_of_words = event.message.text.split(" ")
        id = int(list_of_words[1])  # second (1) item is the id

        # Execute the query to delete the registration with the specific id
        sql_command = "DELETE FROM reg WHERE id = %s"
        crsr.execute(sql_command, (id,))
        conn.commit()  # commit the changes

        # If at least 1 row is affected by the query we send specific messages
        if crsr.rowcount < 1:
            text = "Something went wrong, please try again"
            await client.send_message(SENDER, text, parse_mode='html')
        else:
            text = "Registration successfully deleted!"
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e:
        print(e)
        await client.send_message(SENDER, "Something went wrong... Check your code!", parse_mode='html')
        return
# Command for /reg
@client.on(events.NewMessage(pattern="(?i)/reg"))
async def insert(event):
    try:
        # Get the sender of the message
        sender = await event.get_sender()
        SENDER = sender.id

        # Get the text of the user AFTER the /reg command and split it into a list of words
        list_of_words = event.message.text.split(" ")

        # Check if there are enough words in the message
        if len(list_of_words) < 3:
            await client.send_message(SENDER, "Please provide the name and phone number in the correct format.")
            return

        name = list_of_words[1]  # the second (1) item is the name
        phone = list_of_words[2]  # the third (2) item is the phone number
        email = list_of_words[3]  # the fourth (3) item is the email
        position = list_of_words[4]  # the fifth (4) item is the position

        # Check if the phone number is too long
        if len(phone) > 15:
            await client.send_message(SENDER, "Please provide a phone number with at most 15 digits.")
            return

        # Check if the phone number consists only of digits
        if not phone.isdigit():
            await client.send_message(SENDER, "Please provide a valid phone number consisting only of digits.")
            return

        dt_string = datetime.now().strftime("%d/%m/%Y")  # Use the datetime library to get the date (and format it as DAY/MONTH/YEAR)

        # Create the tuple "params" with all the parameters inserted by the user
        params = (name, phone, email, position, dt_string)
        sql_command = "INSERT INTO reg (Name, Phone, Email, Position, LAST_EDIT) VALUES (%s, %s, %s, %s, %s);"  # the initial NULL is for the AUTOINCREMENT id inside the table
        crsr.execute(sql_command, params)  # Execute the query
        conn.commit()  # commit the changes

        # If at least 1 row is affected by the query we send specific messages
        if crsr.rowcount < 1:
            text = "Something went wrong, please try again"
            await client.send_message(SENDER, text, parse_mode='html')
        else:
            text = "Thank You for registering! Your details have been saved. We will get back to you soon."
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e:
        print(e)
        await client.send_message(SENDER, "Something Wrong happened... Check your code!", parse_mode='html')
        return

# Command for /callback
@client.on(events.NewMessage(pattern="(?i)/callback"))
async def callback(event):
    try:
        # Get the sender of the message
        sender = await event.get_sender()
        SENDER = sender.id

        # Get the text of the user AFTER the /callback command and split it into a list of words
        list_of_words = event.message.text.split(" ")

        # Check if there are enough words in the message
        if len(list_of_words) < 3:
            await client.send_message(SENDER, "Please provide the name and phone number in the correct format.")
            return

        name = list_of_words[1]  # the second (1) item is the name
        phone = list_of_words[2]  # the third (2) item is the phone number

        # Check if the phone number is too long
        if len(phone) > 15:
            await client.send_message(SENDER, "Please provide a phone number with at most 15 digits.")
            return

        # Check if the phone number consists only of digits
        if not phone.isdigit():
            await client.send_message(SENDER, "Please provide a valid phone number consisting only of digits.")
            return

        dt_string = datetime.now().strftime("%d/%m/%Y")  # Use the datetime library to get the date (and format it as DAY/MONTH/YEAR)

        # Create the tuple "params" with all the parameters inserted by the user
        params = (name, phone, dt_string)
        sql_command = "INSERT INTO callback_reg (Name, Phone, LAST_EDIT) VALUES (%s, %s, %s);"  # the initial NULL is for the AUTOINCREMENT id inside the table
        crsr.execute(sql_command, params)  # Execute the query
        conn.commit()  # commit the changes

        # If at least 1 row is affected by the query we send specific messages
        if crsr.rowcount < 1:
            text = "Something went wrong, please try again"
            await client.send_message(SENDER, text, parse_mode='html')
        else:
            text = "Thank You for registering for a callback! We will contact you shortly."
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e:
        print(e)
        await client.send_message(SENDER, "Something Wrong happened... Check your code!", parse_mode='html')
        return

# Function to create message for SELECT query result
def create_message_select_query(res):
    message = "<b>Registered Users:</b>\n\n"
    for row in res:
        message += f"<b>ID:</b> {row[0]}\n"
        message += f"<b>Name:</b> {row[1]}\n"
        message += f"<b>Phone:</b> {row[2]}\n"
        message += f"<b>Email:</b> {row[3]}\n"
        message += f"<b>Position:</b> {row[4]}\n"
        message += f"<b>Last Edited:</b> {row[5]}\n\n"
    return message

# Run the client
create_tables()
print("Bot is running...")
client.run_until_disconnected()
