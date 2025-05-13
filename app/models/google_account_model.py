from .account_info import AccountInfo, AuthProvider


class GoogleAccountModel(AccountInfo):
    authProvider: AuthProvider = "google"
    googleAccountId: str
