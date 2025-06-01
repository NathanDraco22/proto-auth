from .account_info import AccountInfo, AuthProvider


class EmailAccountModel(AccountInfo):
    authProvider: AuthProvider = "email"
    password: str
