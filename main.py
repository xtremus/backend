from sqlite3 import Connection, Row
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import (
    get_admins,
    get_users,
    get_wfh_requests_userid,
    get_pending_wfh_requests_adminid,
    get_approved_wfh_requests_adminid,
    get_rejected_wfh_requests_adminid,
    get_wfh_requests_admin,
    insert_wfh_request,
    edit_wfh_request,
    delete_wfh_request,
    approve_wfh_request,
    reject_wfh_request,
)
from models import (
    Users,
    Edit_WFH_Request,
    WFH_Requests_User,
    WFH_Requests_Admin,
    WFH_Request,
)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = Connection("wfh.db")
connection.row_factory = Row


@app.get("/admins")
async def getAdmins() -> Users:
    return get_admins(connection)


@app.get("/users")
async def getUsers() -> Users:
    return get_users(connection)


@app.get("/wfhRequests")
async def getWfhRequestsbyUserID(userid: int) -> WFH_Requests_User:
    return get_wfh_requests_userid(connection, userid)


@app.get("/adminPendingRequests/{approver_id}")
async def getAdminPendingRequests(approver_id: int) -> WFH_Requests_Admin:
    return get_pending_wfh_requests_adminid(connection, approver_id)


@app.get("/adminApprovedRequests/{approver_id}")
async def getAdminApprovedRequests(approver_id: int) -> WFH_Requests_Admin:
    return get_approved_wfh_requests_adminid(connection, approver_id)


@app.get("/adminRejectedRequests/{approver_id}")
async def getAdminRejectedRequests(approver_id: int) -> WFH_Requests_Admin:
    return get_rejected_wfh_requests_adminid(connection, approver_id)


@app.get("/adminIncomingRequests")
async def getAdminIncomingRequests() -> WFH_Requests_Admin:
    return get_wfh_requests_admin(connection)


@app.post("/addWfhRequest")
async def addWfhRequest(wfh_request: WFH_Request):
    if insert_wfh_request(connection, wfh_request):
        return "WFH request added successfully"
    else:
        return "Failed to add WFH request"


@app.put("/editWfhRequest")
async def editWfhRequest(wfh_request: Edit_WFH_Request):
    if edit_wfh_request(connection, wfh_request):
        return "WFH request edited successfully"
    else:
        return "Failed to edit WFH request"


@app.delete("/deleteWfhRequest/{request_id}")
async def deleteWfhRequest(request_id: int):
    if delete_wfh_request(connection, request_id):
        return "WFH request deleted successfully"
    else:
        return "Failed to delete WFH request"


@app.put("/approveWfhRequest/{request_id}")
async def approveWfhRequest(request_id: int):
    if approve_wfh_request(connection, request_id):
        return "WFH request approved successfully"
    else:
        return "Failed to approve WFH request"


@app.put("/rejectWfhRequest/{request_id}")
async def rejectWfhRequest(request_id: int):
    if reject_wfh_request(connection, request_id):
        return "WFH request rejected successfully"
    else:
        return "Failed to reject WFH request"
