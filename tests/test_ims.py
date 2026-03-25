"""
Unit tests for the Inventory Management System.
All database calls are mocked so tests run without a real MySQL instance.
"""

from unittest.mock import MagicMock, patch, call

# ---------------------------------------------------------------------------
# db_connect
# ---------------------------------------------------------------------------

class TestDbConnect:
    @patch('backend.db_connect.m.connect')
    def test_successful_connection(self, mock_connect):
        """db_connect returns a connection object on success."""
        from backend.db_connect import db_connect
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        result = db_connect()
        assert result == mock_conn

    @patch('backend.db_connect.m.connect')
    def test_failed_connection_returns_none(self, mock_connect):
        """db_connect returns None when MySQL raises an error."""
        import mysql.connector as m
        from backend.db_connect import db_connect
        mock_connect.side_effect = m.Error("Connection refused")
        result = db_connect()
        assert result is None


# ---------------------------------------------------------------------------
# register
# ---------------------------------------------------------------------------

class TestRegister:
    @patch('backend.register.db_connect')
    def test_register_new_user(self, mock_db_connect):
        """Registering a brand-new user commits and returns True."""
        from backend.register import register

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None          # user does not exist
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = register("alice", "securepass123")
        assert result is True
        mock_conn.commit.assert_called_once()

    @patch('backend.register.db_connect')
    def test_register_duplicate_user(self, mock_db_connect):
        """Registering an existing username returns False without committing."""
        from backend.register import register

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'user_id': 1, 'username': 'alice'}
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = register("alice", "anotherpass")
        assert result is False
        mock_conn.commit.assert_not_called()

    @patch('backend.register.db_connect')
    def test_register_db_failure(self, mock_db_connect):
        """Returns False when db_connect returns None."""
        from backend.register import register
        mock_db_connect.return_value = None
        result = register("bob", "pass")
        assert result is False


# ---------------------------------------------------------------------------
# login
# ---------------------------------------------------------------------------

class TestLogin:
    @patch('backend.login.db_connect')
    @patch('backend.login.bcrypt.checkpw', return_value=True)
    def test_successful_login(self, mock_checkpw, mock_db_connect):
        """login returns user dict on valid credentials."""
        from backend.login import login

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            'user_id': 1,
            'username': 'alice',
            'role': 'admin',
            'password_hash': '$2b$12$fakehash'
        }
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = login("alice", "securepass123")
        assert result is not None
        assert result['username'] == 'alice'
        assert result['role'] == 'admin'

    @patch('backend.login.db_connect')
    def test_login_user_not_found(self, mock_db_connect):
        """login returns None when username doesn't exist."""
        from backend.login import login

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = login("ghost", "pass")
        assert result is None

    @patch('backend.login.db_connect')
    @patch('backend.login.bcrypt.checkpw', return_value=False)
    def test_login_wrong_password(self, mock_checkpw, mock_db_connect):
        """login returns None on wrong password."""
        from backend.login import login

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            'user_id': 1,
            'username': 'alice',
            'role': 'staff',
            'password_hash': '$2b$12$fakehash'
        }
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = login("alice", "wrongpass")
        assert result is None


# ---------------------------------------------------------------------------
# inventory
# ---------------------------------------------------------------------------

class TestInventory:
    @patch('backend.inventory.log_transaction')
    @patch('backend.inventory.db_connect')
    def test_additem_success(self, mock_db_connect, mock_log):
        """additem inserts a row, commits, and logs the transaction."""
        from backend.inventory import additem

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 42
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = additem("Widget", 100, "Shelf-A", user_id=1)
        assert result is True
        mock_conn.commit.assert_called_once()
        mock_log.assert_called_once_with(42, 1, "add", 100)

    @patch('backend.inventory.db_connect')
    def test_additem_db_failure(self, mock_db_connect):
        """additem returns False when db_connect returns None."""
        from backend.inventory import additem
        mock_db_connect.return_value = None
        result = additem("Widget", 10, "Shelf-B", user_id=1)
        assert result is False

    @patch('backend.inventory.log_transaction')
    @patch('backend.inventory.db_connect')
    def test_update_quantity_success(self, mock_db_connect, mock_log):
        """update_quantity executes UPDATE and logs an adjust transaction."""
        from backend.inventory import update_quantity

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = update_quantity(item_id=5, new_qty=200, user_id=2)
        assert result is True
        mock_log.assert_called_once_with(5, 2, "adjust", 200)

    @patch('backend.inventory.log_transaction')
    @patch('backend.inventory.db_connect')
    def test_delete_items_success(self, mock_db_connect, mock_log):
        """delete_items logs removal then deletes the row."""
        from backend.inventory import delete_items

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = delete_items(item_id=3, user_id=1)
        assert result is True
        mock_log.assert_called_once_with(3, 1, change_type="remove", quantity_change=0)


# ---------------------------------------------------------------------------
# admin
# ---------------------------------------------------------------------------

class TestAdmin:
    @patch('backend.admin.db_connect')
    def test_change_role_success(self, mock_db_connect):
        """change_role executes UPDATE and commits."""
        from backend.admin import change_role

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = change_role(user_id=2, new_role="admin")
        assert result is True
        mock_conn.commit.assert_called_once()

    @patch('backend.admin.db_connect')
    def test_delete_user_success(self, mock_db_connect):
        """delete_user executes DELETE and commits."""
        from backend.admin import delete_user

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = delete_user(user_id=3)
        assert result is True
        mock_conn.commit.assert_called_once()

    @patch('backend.admin.db_connect')
    def test_change_role_db_failure(self, mock_db_connect):
        """change_role returns False when db_connect returns None."""
        from backend.admin import change_role
        mock_db_connect.return_value = None
        result = change_role(user_id=2, new_role="admin")
        assert result is False


# ---------------------------------------------------------------------------
# transactions
# ---------------------------------------------------------------------------

class TestTransactions:
    @patch('backend.transactions.db_connect')
    def test_log_transaction_success(self, mock_db_connect):
        """log_transaction inserts a row and commits."""
        from backend.transactions import log_transaction

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_conn

        result = log_transaction(item_id=1, user_id=1, change_type="add", quantity_change=50)
        assert result is True
        mock_conn.commit.assert_called_once()

    @patch('backend.transactions.db_connect')
    def test_log_transaction_db_failure(self, mock_db_connect):
        """log_transaction returns False when db_connect returns None."""
        from backend.transactions import log_transaction
        mock_db_connect.return_value = None
        result = log_transaction(1, 1, "add", 10)
        assert result is False
