import api.models.models as apiModels
import database.models.user as DbUserModels

def dbUserDataToApiUserData(user: DbUserModels.User):
    return apiModels.UserData(
        fullname = user.fullname,
        email = user.email
    )

def apiUserToDbUser(user: apiModels.User):
    return DbUserModels.User(
        fullname = user.fullname,
        email = user.email,
        password = user.password
    )
