import random
import Connect_Firebase
import datetime

db_ref = Connect_Firebase.db.collection('DefaultUserToken')

Tokens = {}
lastid = 0

def process():
    length = 32

    lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    special = ['@', '#', '$', '%', '&', '*']
    all = lower + upper + num + special
    ran = random.sample(all,length)
    password = "".join(ran)
    return password


def refresh():
    docs = db_ref.stream()
    global Tokens, lastid
    for doc in docs:
        Tokens[doc.id] = doc.to_dict()
        lastid = int(doc.id.replace("Token", ""))


def Token_check(Token):

    refresh()

    Token = Token[1:-1]

    user_doc_id = None
    LastLoggedIN = datetime.datetime.now().date()
    LastLoggedIN = datetime.datetime.combine(LastLoggedIN, datetime.datetime.min.time())

    for i, j in Tokens.items():
        if j["Token"] == Token:
            user_doc_id = i
            print("Token valid")
            break

    if user_doc_id:
        try:
            db_ref.document(user_doc_id).update({"LastLoggedIN": LastLoggedIN})
            print(f"Last login date successfully updated for user with ID '{user_doc_id}'!")
            return True
        except Exception as e:
            print(f"An error occurred while updating the last login date: {e}")
            return False
    else:
        print("User not found")
        return False



def New_Token(UserId):
    refresh()

    Date_Created = datetime.datetime.now().date().isoformat()
    
    data_list = {
        "Token": process(),
        "Date" : Date_Created,
        "UserID" : UserId
        }
    
    global lastid
    usermainid = f"Token{lastid+1}"
    lastid +=1
    
    doc_ref = db_ref.document(usermainid)
    
    try:
        doc_ref.set(data_list)
        print("called")
        print(f"Document '{usermainid}' successfully written!")
        return data_list["Token"]
    
    except Exception as e:
        return f"An error occurred while writing document '{db_ref}': {e}"


def delete_Token(doc_id):
    doc_ref = db_ref.document(doc_id)
    
    try:
        doc_ref.delete()
        print(f"Document '{doc_id}' successfully deleted!")
        return True
    except Exception as e:
        print(f"An error occurred while deleting document '{doc_id}': {e}")
        return False


def cleanup_old_tokens():
    docs = db_ref.stream()
    today = datetime.datetime.now().date()

    for doc in docs:
        data = doc.to_dict()
        token_date = datetime.datetime.strptime(data['Date'], "%Y-%m-%d").date()
        age = (today - token_date).days

        if age > 15:
            delete_Token(doc.id)
            print(f"Deleted Token '{doc.id}' - it was {age} days old.")
        else:
            print(f"Detected Token '{doc.id}' - it was {age} days old.")

# Call the cleanup function
cleanup_old_tokens()
