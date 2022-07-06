from warrant import *

def make_warrant_requests(api_key):
    client = Warrant(api_key)

    # Create users and session tokens
    print("Created tenant with provided id: " + client.create_tenant("custom_tenant_001"))
    print("Created user with provided id: " + client.create_user("custom_user_001"))
    new_user = client.create_user()
    print("Created user with generated id: " + new_user)
    new_subject = Subject("user", new_user)
    print(client.create_warrant(object_type="tenant", object_id="custom_tenant_001", relation="member", subject=new_subject))
    print("Created session token: " + client.create_session(new_user))

    # Create and check warrants
    print(client.create_warrant(object_type="store", object_id="store1", relation="owner", subject=new_subject))
    subject_to_check = Subject("user", new_user)
    is_authorized = client.is_authorized(object_type="store", object_id="store1", relation="owner", subject_to_check=subject_to_check)
    print(f"New user authorization result: {is_authorized}")
    print(f"All warrants: {client.list_warrants()}")

if __name__ == '__main__':
    # Replace with your Warrant api key
    api_key = "API_KEY"
    make_warrant_requests(api_key)
