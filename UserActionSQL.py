from datetime import datetime
from Mail_Sending import GenerateMail
from Connect_MySQL import db,cursor
import dotenv
dotenv.load_dotenv()
import os


def checkUser(userID, password):
    if "." in userID and "@" in userID:  # Fixed condition
        cursor.execute("SELECT * FROM users WHERE Email = %s AND Password = %s", (userID, password))
        results = cursor.fetchall()

        if results: 
            print("✅ User authenticated successfully!")
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "UPDATE Users SET LastLoggedIN = %s WHERE Email = %s"
            values = (current_time, userID)
            cursor.execute(query, values)
            db.commit()  # Save changes to the database
            print(f"🕒 Updated HomeID {userID} with datetime: {current_time}")
        else:
            print("❌ Invalid credentials!")
    else:
        cursor.execute("SELECT * FROM users WHERE UserID = %s AND Password = %s", (userID, password))
        results = cursor.fetchall()
        if results:
            print("✅ User authenticated successfully!")
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "UPDATE Users SET LastLoggedIN = %s WHERE UserID = %s" 
            values = (current_time, userID)
            cursor.execute(query, values)
            db.commit()
            print(f"🕒 Updated HomeID {userID} with datetime: {current_time}")
        else:
            print("❌ Invalid credentials!")


def forgotPassword(Email):
    cursor.execute("SELECT * FROM Users WHERE Email = %s", (Email,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("User Found! Sending OTP")
        otp = GenerateMail(Email)
        query = "UPDATE Users SET otp = %s WHERE Email = %s"
        values = (otp, Email)

        cursor.execute(query, values)
        db.commit()
        return "User Found! Sending OTP"
    else:
        print("Email does not Exist")
        return "Email does not Exist"


def ResetPassword(Email, OTP, NewPassword):
    cursor.execute("SELECT * FROM Users WHERE Email = %s AND OTP = %s", (Email, OTP))
    existing_user = cursor.fetchone()
    if existing_user:
        print("✅ OTP verified successfully!")
        cursor.execute("UPDATE Users SET Password = %s WHERE Email = %s", (NewPassword, Email))
        db.commit()
        print("✅ Password updated successfully!")
        return "✅ Password updated successfully!"
    else:
        print("❌ Invalid OTP!")
        return "❌ Invalid OTP!"

def New_User(Username, UserID, Password,HomeID, Email, Contact,Address,Region):
    cursor.execute("SELECT * FROM Users WHERE UserID = %s OR Email = %s", (UserID, Email))
    existing_user = cursor.fetchone()
    
    if existing_user:
        print("❌ UserID or Email already exists!")
        return "❌ UserID or Email already exists!"
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO Users (Username, UserID, Password, Email, HomeID, Contact, DateCreated, LastLoggedIN, Address, Region) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (Username, UserID, Password, Email, HomeID, Contact, current_time, current_time, Address, Region)

    cursor.execute(query, values)
    db.commit()

    print(f"✅ User '{UserID}' successfully registered!")
    return "User successfully registered!"


# New_User("Satwik", "Alkyemaq", "Satwik@890", "satwik@a.com", "9876543210")
# checkUser("Alkyema","Satwik@890")
# ResetPassword("satwikkishore6953@gmail.com",682869,"Satwik@890")
cursor.close()
db.close()


