from models import User, Order
from main import Session

# with Session() as session:
#     User creation:
#
#     new_user = User(username='john_doe', email='john@example.com')
#     session.add(new_user)
#     session.commit()
#
#     new_user = User(username='jane_doe', email='jane@example.com')
#     session.add(new_user)
#     session.commit()
#
#     new_user = User(username='alice_peterson', email='alice@example.com')
#     session.add(new_user)
#     session.commit()
#
#     Retrieve already created users:
#
#     users = session.query(User).all()
#     for user in users:
#         print(str(user))
#
#     Update user:
#
#     user_to_update = session.query(User).filter_by(username=input("Enter username to match: ")).first()
#
#     if user_to_update:
#         user_to_update.email = input("Enter new email: ")
#         session.commit()
#         print(f"Email of {user_to_update.username} updated successfully!")
#     else:
#         print(f"User not found!")
#
#     Delete user:
#
#     user_to_delete = session.query(User).filter_by(username=input("Enter username to match: ")).first()
#
#     if user_to_delete:
#         session.delete(user_to_delete)
#         session.commit()
#         print(f"User {user_to_delete.username} deleted successfully!")
#     else:
#         print(f"User not found!")

# with Session() as session:
#     session.add_all([Order(user_id=i) for i in range(9, 14)])
#     session.commit()

with Session() as session:
    orders = session.query(Order).order_by(Order.user_id.desc()).all()

    if not orders:
        print("No orders made yet!")
    else:
        for order in orders:
            user = order.user
            print(f"Order number {order.id}, "
                  f"Is completed: {order.is_completed}, "
                  f"Username: {user.username}")
