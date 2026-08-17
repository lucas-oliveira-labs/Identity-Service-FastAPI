from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, status

from src.services.user_service import UserService


@pytest.fixture
def service():
    return UserService()


@pytest.fixture
def user_create():
    user = MagicMock()
    user.nome = "Lucas"
    user.email = "lucas@example.com"
    user.password = "senha123"
    return user


@pytest.fixture
def user_update():
    user = MagicMock()
    user.nome = "Lucas Atualizado"
    user.email = "novo@example.com"
    return user


@pytest.fixture
def user_password_update():
    password = MagicMock()
    password.senha_atual = "senha-atual"
    password.nova_senha = "nova-senha"
    return password


@pytest.mark.asyncio
async def test_create_user_success(service, user_create):
    query = MagicMock()
    query.first = AsyncMock(return_value=None)

    new_user = MagicMock()

    with (
        patch(
            "src.services.user_service.User.filter",
            return_value=query,
        ) as mock_filter,
        patch(
            "src.services.user_service.hash_password",
            return_value="hashed-password",
        ) as mock_hash,
        patch(
            "src.services.user_service.User.create",
            new_callable=AsyncMock,
            return_value=new_user,
        ) as mock_create,
    ):
        result = await service.create_user(user_create)

    assert result is new_user

    mock_filter.assert_called_once_with(email="lucas@example.com")
    query.first.assert_awaited_once()

    mock_hash.assert_called_once_with("senha123")

    mock_create.assert_awaited_once_with(
        nome="Lucas",
        email="lucas@example.com",
        password_hash="hashed-password",
    )


@pytest.mark.asyncio
async def test_create_user_email_already_exists(service, user_create):
    existing_user = MagicMock()

    query = MagicMock()
    query.first = AsyncMock(return_value=existing_user)

    with (
        patch(
            "src.services.user_service.User.filter",
            return_value=query,
        ),
        patch(
            "src.services.user_service.User.create",
            new_callable=AsyncMock,
        ) as mock_create,
        pytest.raises(HTTPException) as exc,
    ):
        await service.create_user(user_create)

    assert exc.value.status_code == status.HTTP_409_CONFLICT
    assert exc.value.detail == "Email já cadastrado"

    mock_create.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_all_users(service):
    users = [MagicMock(), MagicMock()]

    with patch(
        "src.services.user_service.User.all",
        new_callable=AsyncMock,
        return_value=users,
    ) as mock_all:
        result = await service.get_all_users()

    assert result == users
    mock_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_id(service):
    user = MagicMock()

    query = MagicMock()
    query.first = AsyncMock(return_value=user)

    with patch(
        "src.services.user_service.User.filter",
        return_value=query,
    ) as mock_filter:
        result = await service.get_user_by_id(10)

    assert result is user

    mock_filter.assert_called_once_with(id=10)
    query.first.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(service):
    query = MagicMock()
    query.first = AsyncMock(return_value=None)

    with patch(
        "src.services.user_service.User.filter",
        return_value=query,
    ):
        result = await service.get_user_by_id(999)

    assert result is None


@pytest.mark.asyncio
async def test_get_user_me(service):
    current_user = MagicMock()

    result = await service.get_user_me(current_user)

    assert result is current_user


@pytest.mark.asyncio
async def test_put_user_by_id_success(service, user_update):
    existing_user = MagicMock()
    existing_user.save = AsyncMock()

    query = MagicMock()
    query.first = AsyncMock(return_value=existing_user)

    with patch(
        "src.services.user_service.User.filter",
        return_value=query,
    ) as mock_filter:
        result = await service.put_user_by_id(1, user_update)

    assert result is existing_user
    assert existing_user.nome == "Lucas Atualizado"
    assert existing_user.email == "novo@example.com"

    mock_filter.assert_called_once_with(id=1)
    query.first.assert_awaited_once()
    existing_user.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_put_user_by_id_not_found(service, user_update):
    query = MagicMock()
    query.first = AsyncMock(return_value=None)

    with (
        patch(
            "src.services.user_service.User.filter",
            return_value=query,
        ),
        pytest.raises(HTTPException) as exc,
    ):
        await service.put_user_by_id(999, user_update)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Usuário não encontrado"


@pytest.mark.asyncio
async def test_put_user_me_email_success(service, user_update):
    current_user = MagicMock()
    current_user.id = 1
    current_user.nome = "Nome antigo"
    current_user.email = "old@example.com"
    current_user.save = AsyncMock()

    query = MagicMock()
    query.exclude.return_value.exists = AsyncMock(return_value=False)

    with patch(
        "src.services.user_service.User.filter",
        return_value=query,
    ) as mock_filter:
        result = await service.put_user_me(
            current_user,
            user_update,
        )

    assert result is current_user
    assert current_user.email == "novo@example.com"
    assert current_user.nome == "Lucas Atualizado"

    mock_filter.assert_called_once_with(email="novo@example.com")
    query.exclude.assert_called_once_with(id=1)
    query.exclude.return_value.exists.assert_awaited_once()

    current_user.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_put_user_me_email_already_exists(service, user_update):
    current_user = MagicMock()
    current_user.id = 1

    query = MagicMock()
    query.exclude.return_value.exists = AsyncMock(return_value=True)

    with (
        patch(
            "src.services.user_service.User.filter",
            return_value=query,
        ),
        pytest.raises(HTTPException) as exc,
    ):
        await service.put_user_me(
            current_user,
            user_update,
        )

    assert exc.value.status_code == status.HTTP_409_CONFLICT
    assert exc.value.detail == "Email já cadastrado"


@pytest.mark.asyncio
async def test_put_user_me_only_name(service):
    current_user = MagicMock()
    current_user.id = 1
    current_user.nome = "Nome antigo"
    current_user.email = "email@example.com"
    current_user.save = AsyncMock()

    user = MagicMock()
    user.email = None
    user.nome = "Novo Nome"

    with patch(
        "src.services.user_service.User.filter",
    ) as mock_filter:
        result = await service.put_user_me(
            current_user,
            user,
        )

    assert result is current_user
    assert current_user.nome == "Novo Nome"
    assert current_user.email == "email@example.com"

    mock_filter.assert_not_called()
    current_user.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_put_user_me_only_email(service):
    current_user = MagicMock()
    current_user.id = 1
    current_user.nome = "Nome"
    current_user.email = "old@example.com"
    current_user.save = AsyncMock()

    user = MagicMock()
    user.email = "new@example.com"
    user.nome = None

    query = MagicMock()
    query.exclude.return_value.exists = AsyncMock(return_value=False)

    with patch(
        "src.services.user_service.User.filter",
        return_value=query,
    ):
        result = await service.put_user_me(
            current_user,
            user,
        )

    assert result is current_user
    assert current_user.email == "new@example.com"
    assert current_user.nome == "Nome"

    current_user.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_put_user_me_without_changes(service):
    current_user = MagicMock()
    current_user.id = 1
    current_user.nome = "Nome"
    current_user.email = "email@example.com"
    current_user.save = AsyncMock()

    user = MagicMock()
    user.email = None
    user.nome = None

    with patch(
        "src.services.user_service.User.filter",
    ) as mock_filter:
        result = await service.put_user_me(
            current_user,
            user,
        )

    assert result is current_user
    assert current_user.nome == "Nome"
    assert current_user.email == "email@example.com"

    mock_filter.assert_not_called()
    current_user.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_password_success(
    service,
    user_password_update,
):
    current_user = MagicMock()
    current_user.password_hash = "old-hash"
    current_user.save = AsyncMock()

    with (
        patch(
            "src.services.user_service.verify_password",
            return_value=True,
        ) as mock_verify,
        patch(
            "src.services.user_service.hash_password",
            return_value="new-hash",
        ) as mock_hash,
    ):
        result = await service.update_password(
            current_user,
            user_password_update,
        )

    assert result is None
    assert current_user.password_hash == "new-hash"

    mock_verify.assert_called_once_with(
        "senha-atual",
        "old-hash",
    )

    mock_hash.assert_called_once_with(
        "nova-senha",
    )

    current_user.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_password_invalid_current_password(
    service,
    user_password_update,
):
    current_user = MagicMock()
    current_user.password_hash = "old-hash"
    current_user.save = AsyncMock()

    with (
        patch(
            "src.services.user_service.verify_password",
            return_value=False,
        ) as mock_verify,
        pytest.raises(HTTPException) as exc,
    ):
        await service.update_password(
            current_user,
            user_password_update,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Senha atual inválida"

    mock_verify.assert_called_once_with(
        "senha-atual",
        "old-hash",
    )

    current_user.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_user_by_id_success(service):
    user = MagicMock()
    user.delete = AsyncMock()

    with patch(
        "src.services.user_service.User.get_or_none",
        new_callable=AsyncMock,
        return_value=user,
    ) as mock_get:
        result = await service.delete_user_by_id(1)

    assert result is None

    mock_get.assert_awaited_once_with(id=1)
    user.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_by_id_not_found(service):
    with (
        patch(
            "src.services.user_service.User.get_or_none",
            new_callable=AsyncMock,
            return_value=None,
        ) as mock_get,
        pytest.raises(HTTPException) as exc,
    ):
        await service.delete_user_by_id(999)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Usuário não encontrado"

    mock_get.assert_awaited_once_with(id=999)
