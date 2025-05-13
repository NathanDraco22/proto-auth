from models.account_info import AccountInfo
from core.token_manager import TokenManager


def generate_token(account: AccountInfo) -> tuple[str, str]:
    """Generate access and refresh tokens, respectively."""
    refresh_token = TokenManager.generate_refresh_token(
        account.id,
        {"emailVerified": account.isEmailVerified},
    )
    access_token = TokenManager.generate_access_token(
        account.id,
        {"emailVerified": account.isEmailVerified},
    )
    return access_token, refresh_token
