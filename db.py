import sqlite3
from sqlite3 import Connection
from typing import List
from models import (
    User,
    Users,
    WFH_Request,
    Edit_WFH_Request,
    WFH_Request_User,
    WFH_Requests_User,
    WFH_Request_Admin,
    WFH_Requests_Admin,
)
from datetime import datetime


def get_admins(connection: Connection) -> Users:
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE role = 'Admin'")
        return Users(users=[User.model_validate(dict(user)) for user in cursor])


def get_users(connection: Connection) -> Users:
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE role = 'User'")
        return Users(users=[User.model_validate(dict(user)) for user in cursor])


def get_wfh_requests_userid(connection: Connection, user_id: int) -> WFH_Requests_User:
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "w.request_id, "
            "w.from_datetime, "
            "w.to_datetime, "
            "w.status, "
            "w.created_at, "
            "w.approver_id, "
            "a.name AS approver_name, "
            "a.email AS approver_email "
            "FROM WFH_Requests w JOIN Users a "
            "ON w.approver_id = a.user_id "
            "WHERE w.user_id = :user_id "
            "ORDER BY w.from_datetime DESC",
            {"user_id": user_id},
        )
        return WFH_Requests_User(
            requests=[
                WFH_Request_User.model_validate(dict(request)) for request in cursor
            ]
        )


def get_wfh_requests_admin(connection: Connection) -> WFH_Requests_Admin:
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT WFH_Requests.request_id, Users.name, Users.email, WFH_Requests.from_datetime, WFH_Requests.to_datetime, WFH_Requests.status, WFH_Requests.created_at FROM WFH_Requests JOIN Users ON WFH_Requests.user_id = Users.user_id"
        )
        return WFH_Requests_Admin(
            requests=[
                WFH_Request_Admin.model_validate(dict(request)) for request in cursor
            ]
        )


def get_rejected_wfh_requests_adminid(
    connection: Connection, approver_id: int
) -> WFH_Requests_Admin:
    return get_wfh_requests_adminid(connection, approver_id, "Rejected")


def get_approved_wfh_requests_adminid(
    connection: Connection, approver_id: int
) -> WFH_Requests_Admin:
    return get_wfh_requests_adminid(connection, approver_id, "Approved")


def get_pending_wfh_requests_adminid(
    connection: Connection, approver_id: int
) -> WFH_Requests_Admin:
    return get_wfh_requests_adminid(connection, approver_id, "New")


def get_wfh_requests_adminid(
    connection: Connection, approver_id: int, status: str
) -> WFH_Requests_Admin:
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT WFH_Requests.request_id, Users.name, Users.email, WFH_Requests.from_datetime, WFH_Requests.to_datetime, WFH_Requests.status, WFH_Requests.created_at FROM WFH_Requests JOIN Users ON WFH_Requests.user_id = Users.user_id WHERE WFH_Requests.approver_id = :approver_id AND WFH_Requests.status = :status ORDER BY WFH_Requests.from_datetime DESC",
            {"approver_id": approver_id, "status": status},
        )
        return WFH_Requests_Admin(
            requests=[
                WFH_Request_Admin.model_validate(dict(request)) for request in cursor
            ]
        )


def insert_wfh_request(connection: Connection, wfh_req: WFH_Request):
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO WFH_Requests (user_id, from_datetime, to_datetime, approver_id) VALUES (:user_id, :from_datetime, :to_datetime, :approver_id)",
                wfh_req.model_dump(),
            )
            rows_affected = cursor.rowcount
            return rows_affected > 0
    except Exception as e:
        print(f"Error adding WFH request: {e}")
        return False


def edit_wfh_request(connection: Connection, wfh_req: Edit_WFH_Request):
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE WFH_Requests SET from_datetime = :from_datetime, to_datetime = :to_datetime, approver_id = :approver_id , updated_at = CURRENT_TIMESTAMP WHERE request_id = :request_id",
                wfh_req.model_dump(),
            )
            rows_affected = cursor.rowcount
            return rows_affected > 0
    except Exception as e:
        print(f"Error editing WFH request: {e}")
        return False


def delete_wfh_request(connection: Connection, request_id: int) -> bool:
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM WFH_Requests WHERE request_id = :request_id",
                {"request_id": request_id},
            )
            rows_affected = cursor.rowcount
            return rows_affected > 0
    except Exception as e:
        print(f"Error deleting WFH request: {e}")
        return False


def approve_wfh_request(connection: Connection, request_id: int) -> bool:
    return update_wfh_request(connection, request_id, "Approved")


def reject_wfh_request(connection: Connection, request_id: int) -> bool:
    return update_wfh_request(connection, request_id, "Rejected")


def update_wfh_request(connection: Connection, request_id: int, status: str) -> bool:
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE WFH_Requests SET status = :status , updated_at = CURRENT_TIMESTAMP WHERE request_id = :request_id",
                {"status": status, "request_id": request_id},
            )
            rows_affected = cursor.rowcount
            return rows_affected > 0
    except Exception as e:
        print(f"Error updating WFH request: {e}")
        return False


if __name__ == "__main__":
    connection = sqlite3.connect("wfh.db")
    connection.row_factory = sqlite3.Row
    # wfh_req = WFH_Request(
    #     user_id=1,
    #     from_datetime=datetime.strptime("2024-10-16 09:00:00", "%Y-%m-%d %H:%M:%S"),
    #     to_datetime=datetime.strptime("2024-10-16 17:00:00", "%Y-%m-%d %H:%M:%S"),
    #     approver_id=2,
    # )

    # insert_wfh_request(connection, wfh_req)

    # print(get_wfh_requests_admin(connection))
    success = update_wfh_request(connection, 0, "New")
    if success:
        print("WFH request updated successfully")
    else:
        print("Failed to update WFH request")

    # print(get_users(connection))
    # for wfh_request in get_wfh_requests_admin(connection):
    #     print(dict(wfh_request))
