import typing


def get_repository(repo_type: typing.Type) -> typing.Callable:
    """
    Simplified repository dependency injection for Supabase-based repositories.
    Repositories no longer need database sessions.
    """
    def _get_repo() -> typing.Any:
        return repo_type()

    return _get_repo
