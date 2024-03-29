from pydantic import EmailStr
from fastapi import status, HTTPException, Request
features.users import user_enums
from bson import ObjectId


def rais_exeption(status_code: status, message: str, exception: Exception = None):
    """
    Raises an HTTPException with the given status code and message.

    Args:
        status_code (status): The status code for the HTTPException.
        message (str): The detail message for the HTTPException.

    Raises:
        HTTPException: An exception with the provided status code and detail message.
    """
    if exception:
        message = f"{message} Original exception: {repr(exception)}"
    raise HTTPException(status_code=status_code, detail=message)


def find_account_by_email(request: Request, email: EmailStr):
    """
    Finds a user account by the provided email in the database.

    Args:
        request (Request): The request object containing the database connection.
        email (EmailStr): The email of the user account to find.

    Returns:
        dict: The found user account, or None if no user is found.
    """
    return request.app.database["users"].find_one({"email": email})


def find_account_by_id(request: Request, id: str):
    """
    Finds a user account by the provided id in the database.

    Args:
        request (Request): The request object containing the database connection.
        id (str): The id of the user account to find.

    Returns:
        dict: The found user account, or None if no user is found.
    """
    object_id = ObjectId(id)
    return request.app.database["users"].find_one({"_id": object_id})


def change_account_status(request: Request, id: str, status: user_enums):
    """
    Changes the status of a user account in the database.

    Args:
        request (Request): The request object containing the database connection.
        id (str): The id of the user account to update.
        status (user_enums): The new status for the user account.
    """
    request.app.database["users"].update_one(
        {"_id": id}, {"$set": {"status": status}})
    return find_account_by_id(request, id)


def change_account_role(request: Request, id: ObjectId, role: user_enums.UserStatus):
    """
    ADMIN-ONLY
    Changes the role of a user account in the database.

    Args:
        request (Request): The request object containing the database connection.
        id (str): The id of the user account to update.
        status (user_enums): The new status for the user account.
    """
    user = request.app.database["users"].update_one(
        {"_id": id}, {"$set": {"role": role}})
    update_user = find_account_by_id(request, id)
    # print('update_user')
    # print(update_user)
    return update_user


### *###**###*###
## USED IN DB ##
### *###**###*###


def avtivate_account(request: Request, email: EmailStr):
    """
    Activates a user account by changing its status in the database to 'active'.

    Args:
        request (Request): The request object containing the database connection.
        email (EmailStr): The email of the user account to activate.

    Raises:
        HTTPException: An exception if an error occurred during the activation process.
    """

    targeted_user = find_account_by_email(request, email)
    if targeted_user:
        try:
            user = change_account_status(
                request, targeted_user['_id'], "active")
            return user
        except Exception as e:
            rais_exeption(
                status.HTTP_304_NOT_MODIFIED, "an error occured while activating your account, please try again later, or contact supporrt.")
