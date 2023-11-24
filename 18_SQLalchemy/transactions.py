from main import Session
from models import User

# Sample data
sample_data = [
    {'username': 'john_doe', 'email': 'john.doe@example.com'},
    {'username': 'sarah_smith', 'email': 'sarah.smith@gmail.com'},
    {'username': 'mike_jones', 'email': 'mike.jones@company.com'},
    {'username': 'emma_wilson', 'email': 'emma.wilson@domain.net'},
    {'username': 'david_brown', 'email': 'david.brown@email.org'},
]

# with Session() as session:
#     try:
#         # Use add_all() to add the sample data to the "users" table
#         session.add_all([User(username=user['username'], email=user['email']) for user in sample_data])
#
#         # Commit the transaction
#         session.commit()
#         print("Data added to 'users' table successfully.")
#
#     except Exception as e:
#         # Rollback the transaction in case of an error
#         session.rollback()
#         print(f"Error in transaction: {str(e)}")
#
#     finally:
#         # Close the session
#         session.close()

# with Session() as session:
#     try:
#         session.begin()
#         session.query(User).delete()
#         session.commit()
#         print("Deleted all user successfully!")
#     except Exception as e:
#         session.rollback()
#         print("Error occurred! ", str(e))
#     finally:
#         session.close()
