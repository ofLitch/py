import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

class SubscriberDAO:
    def __init__(self):
        """Initialize the database connection."""
        try:
            # Load database config from JSON file
            #3with open("config.json") as config_file:
            #    config = json.load(config_file)
            self.connection = mysql.connector.connect(
                host="localhost",
                database="subscriber_network",
                user="root",
                password="omcaicedo"
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def find_all_friends(self, subscriber_id):
        """Find all friends of a given subscriber."""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT s.name AS friend_name
            FROM friend f
            JOIN subscriber s ON f.friend_id = s.subscriber_id
            WHERE f.subscriber_id = %s
            """
            cursor.execute(query, (subscriber_id,))
            friends = cursor.fetchall()
            cursor.close()
            return friends
        except Error as e:
            print(f"Error fetching friends: {e}")
            return []

    def get_messages_between_subscribers(self, subscriber_id_1, subscriber_id_2):
        """Get all messages exchanged between two subscribers."""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT m.message_text, s1.name AS sender_name, s2.name AS recipient_name, m.sent_at
            FROM message m
            JOIN subscriber s1 ON m.sender_id = s1.subscriber_id
            JOIN subscriber s2 ON m.recipient_id = s2.subscriber_id
            WHERE (m.sender_id = %s AND m.recipient_id = %s)
               OR (m.sender_id = %s AND m.recipient_id = %s)
            ORDER BY m.sent_at
            """
            cursor.execute(query, (subscriber_id_1, subscriber_id_2, subscriber_id_2, subscriber_id_1))
            messages = cursor.fetchall()
            cursor.close()
            return messages
        except Error as e:
            print(f"Error fetching messages: {e}")
            return []

    def find_messages_sent_by_subscriber(self, subscriber_id):
        """Find all messages sent by a specific subscriber."""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT m.message_text, s.name AS recipient_name, m.sent_at
            FROM message m
            JOIN subscriber s ON m.recipient_id = s.subscriber_id
            WHERE m.sender_id = %s
            ORDER BY m.sent_at
            """
            cursor.execute(query, (subscriber_id,))
            messages = cursor.fetchall()
            cursor.close()
            return messages
        except Error as e:
            print(f"Error fetching messages: {e}")
            return []

    ### CRUD Operations for Subscriber Table ###
    def insert_subscriber(self, identifier, name, email, ip, port):
        """
        Insert subscriber information into the database and register the connection details with a timestamp.
        """
        db = self.connect_db()
        if db is None:
            return

        cursor = db.cursor()

        # Obtener el timestamp actual
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Insertar suscriptor
            cursor.execute("INSERT INTO subscribers (identifier, name, email) VALUES (%s, %s, %s)",
                            (identifier, name, email))
            subscriber_id = cursor.lastrowid

            # Insertar conexión con timestamp
            cursor.execute("INSERT INTO connections (subscriber_id, ip_address, port, timestamp) VALUES (%s, %s, %s, %s)",
                            (subscriber_id, ip, port, current_timestamp))

            db.commit()
            print(f"Subscriber {name} added with ID {subscriber_id} at {current_timestamp}.")
        except mysql.connector.Error as e:
            print(f"Error inserting subscriber: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def delete_subscriber(self, subscriber_id):
        """Delete a subscriber by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM subscriber WHERE subscriber_id = %s"
            cursor.execute(query, (subscriber_id,))
            self.connection.commit()
            print(f"Subscriber {subscriber_id} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting subscriber: {e}")

    def update_subscriber(self, subscriber_id, name=None, email=None):
        """Update subscriber details by ID."""
        try:
            cursor = self.connection.cursor()
            if name and email:
                query = "UPDATE subscriber SET name = %s, email = %s WHERE subscriber_id = %s"
                cursor.execute(query, (name, email, subscriber_id))
            elif name:
                query = "UPDATE subscriber SET name = %s WHERE subscriber_id = %s"
                cursor.execute(query, (name, subscriber_id))
            elif email:
                query = "UPDATE subscriber SET email = %s WHERE subscriber_id = %s"
                cursor.execute(query, (email, subscriber_id))
            self.connection.commit()
            print(f"Subscriber {subscriber_id} updated successfully.")
            cursor.close()
        except Error as e:
            print(f"Error updating subscriber: {e}")

    def select_subscriber(self, subscriber_id):
        """Select a subscriber by ID."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM subscriber WHERE subscriber_id = %s"
            cursor.execute(query, (subscriber_id,))
            subscriber = cursor.fetchone()
            cursor.close()
            return subscriber
        except Error as e:
            print(f"Error selecting subscriber: {e}")
            return None

    ### CRUD Operations for Friend Table ###
    def insert_friend(self, subscriber_id, friend_id):
        """Insert a friendship relation between two subscribers."""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO friend (subscriber_id, friend_id) VALUES (%s, %s)"
            cursor.execute(query, (subscriber_id, friend_id))
            self.connection.commit()
            print(f"Friendship between {subscriber_id} and {friend_id} inserted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error inserting friend: {e}")

    def delete_friend(self, subscriber_id, friend_id):
        """Delete a friendship relation."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM friend WHERE subscriber_id = %s AND friend_id = %s"
            cursor.execute(query, (subscriber_id, friend_id))
            self.connection.commit()
            print(f"Friendship between {subscriber_id} and {friend_id} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting friend: {e}")

    def select_all_friends(self, subscriber_id):
        """Select all friends of a subscriber."""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT s.subscriber_id, s.name, s.email 
            FROM friend f 
            JOIN subscriber s ON f.friend_id = s.subscriber_id 
            WHERE f.subscriber_id = %s
            """
            cursor.execute(query, (subscriber_id,))
            friends = cursor.fetchall()
            cursor.close()
            return friends
        except Error as e:
            print(f"Error selecting friends: {e}")
            return []

    ### CRUD Operations for Message Table ###
    def insert_message(self, sender_id, recipient_id, message_text):
        """Insert a message between two subscribers."""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO message (sender_id, recipient_id, message_text) VALUES (%s, %s, %s)"
            cursor.execute(query, (sender_id, recipient_id, message_text))
            self.connection.commit()
            print(f"Message from {sender_id} to {recipient_id} inserted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error inserting message: {e}")

    def delete_message(self, message_id):
        """Delete a message by ID."""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM message WHERE message_id = %s"
            cursor.execute(query, (message_id,))
            self.connection.commit()
            print(f"Message {message_id} deleted successfully.")
            cursor.close()
        except Error as e:
            print(f"Error deleting message: {e}")

    def update_message(self, message_id, new_text):
        """Update the content of a message."""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE message SET message_text = %s WHERE message_id = %s"
            cursor.execute(query, (new_text, message_id))
            self.connection.commit()
            print(f"Message {message_id} updated successfully.")
            cursor.close()
        except Error as e:
            print(f"Error updating message: {e}")

    def select_message(self, message_id):
        """Select a message by ID."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM message WHERE message_id = %s"
            cursor.execute(query, (message_id,))
            message = cursor.fetchone()
            cursor.close()
            return message
        except Error as e:
            print(f"Error selecting message: {e}")
            return None