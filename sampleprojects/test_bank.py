import os
import sys
import io
import unittest
from unittest.mock import patch

# Temporarily add the directory of the main application to the path
# This assumes banking_application.py is in the same directory as this test file
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import functions from the main banking application
# Make sure your main file is named 'banking_application.py'
from banking_application import (
    create_account,
    deposit,
    withdraw,
    currency_converter,
    view_transaction_history,
    read_accounts,
    save_accounts,
    EMAIL_INBOX_FILE,
    MESSAGES_INBOX_FILE,
    ACCOUNTS_FILE,
    TRANSACTIONS_FILE,
    USD_TO_KES_RATE
)

# --- Setup for Testing ---
TEST_ACCOUNTS_FILE = "test_bank_accounts.csv"
TEST_TRANSACTIONS_FILE = "test_transactions.csv"
TEST_EMAIL_INBOX_FILE = "test_email_inbox.txt"
TEST_MESSAGES_INBOX_FILE = "test_messages_inbox.txt"

# Override the file paths in the main module for testing
# This ensures tests don't interfere with actual user data files
def setup_test_files():
    global ACCOUNTS_FILE, TRANSACTIONS_FILE, EMAIL_INBOX_FILE, MESSAGES_INBOX_FILE
    ACCOUNTS_FILE = TEST_ACCOUNTS_FILE
    TRANSACTIONS_FILE = TEST_TRANSACTIONS_FILE
    EMAIL_INBOX_FILE = TEST_EMAIL_INBOX_FILE
    MESSAGES_INBOX_FILE = TEST_MESSAGES_INBOX_FILE
    # Ensure test files are clean before each test run
    for f in [ACCOUNTS_FILE, TRANSACTIONS_FILE, EMAIL_INBOX_FILE, MESSAGES_INBOX_FILE]:
        if os.path.exists(f):
            os.remove(f)

def teardown_test_files():
    for f in [TEST_ACCOUNTS_FILE, TEST_TRANSACTIONS_FILE, TEST_EMAIL_INBOX_FILE, TEST_MESSAGES_INBOX_FILE]:
        if os.path.exists(f):
            os.remove(f)

class TestBankingApp(unittest.TestCase):

    def setUp(self):
        """Set up for each test: ensure clean test files."""
        setup_test_files()
        # Re-import to ensure global variables are updated for each test
        # This is a bit hacky but works for simple global overrides
        import banking_application
        banking_application.ACCOUNTS_FILE = TEST_ACCOUNTS_FILE
        banking_application.TRANSACTIONS_FILE = TEST_TRANSACTIONS_FILE
        banking_application.EMAIL_INBOX_FILE = TEST_EMAIL_INBOX_FILE
        banking_application.MESSAGES_INBOX_FILE = TEST_MESSAGES_INBOX_FILE

    def tearDown(self):
        """Clean up after each test: remove test files."""
        teardown_test_files()

    @patch('builtins.input', side_effect=[
        'testuser1', 'password123', 'password123', # Username, password
        'dog', 'cat', # Security questions answers
        'Test User One', 'Kenyan', '+254', '712345678', 'test1@example.com', 'A123B456C',
        'Savings', 'Engineer', 'Salary', 5, 2, 1000.0, '123 Main St', 1, # Personal details, branch
        '1', # Account type: Current Bank account (no opening balance)
        '123456' # OTP
    ])
    def test_1_create_account_active(self, mock_input):
        """Test account creation for an account type with no opening balance."""
        print("\n--- Testing Account Creation (Active) ---")
        result = create_account()
        self.assertTrue(result, "Account creation should succeed for active account.")
        accounts = read_accounts()
        self.assertIn('testuser1', accounts)
        self.assertEqual(accounts['testuser1']['password'], 'password123')
        self.assertEqual(accounts['testuser1']['balance'], 0.0) # Starts at 0
        self.assertEqual(accounts['testuser1']['details']['account_status'], 'Active')
        print("Account 'testuser1' created and activated successfully.")

    @patch('builtins.input', side_effect=[
        'testuser2', 'password456', 'password456', # Username, password
        'fish', 'bird', # Security questions answers
        'Test User Two', 'Ugandan', '+256', '777888999', 'test2@example.com', 'D789E012F',
        'Investment', 'Doctor', 'Business', 10, 5, 5000.0, '456 Oak Ave', 4, # Personal details, branch, Sapphire Multi currency
        '4', # Account type: Sapphire Multi currency account (requires opening balance)
        'yes', # Confirm account type
        '789012' # OTP
    ])
    def test_2_create_account_activation_needed(self, mock_input):
        """Test account creation for an account type requiring opening balance."""
        print("\n--- Testing Account Creation (Activation Needed) ---")
        result = create_account()
        self.assertTrue(result, "Account creation should succeed for activation needed account.")
        accounts = read_accounts()
        self.assertIn('testuser2', accounts)
        self.assertEqual(accounts['testuser2']['details']['account_status'], 'Activation needed')
        print("Account 'testuser2' created with 'Activation needed' status.")

    @patch('builtins.input', side_effect=[
        'testuser1', # Username for deposit
        'password123', # Passcode for deposit (assuming it's set later or default)
        '1', # Select Default Test Wallet
        '50.0' # Amount to deposit
    ])
    @patch('banking_application.send_payment_otp_sms', return_value=True) # Mock OTP sending
    def test_3_deposit_function(self, mock_send_sms, mock_input):
        """Test the deposit function."""
        print("\n--- Testing Deposit Function ---")
        # First, create a user with a payment passcode for deposit to work
        with patch('builtins.input', side_effect=[
            'deposituser', 'depopass', 'depopass', # Username, password
            'dog', 'cat', # Security questions answers
            'Deposit User', 'Kenyan', '+254', '711223344', 'depo@example.com', 'G111H222I',
            'Savings', 'Clerk', 'Salary', 2, 1, 500.0, '789 Pine St', 1, # Personal details
            '1', # Account type: Current Bank account
            '123456' # OTP
        ]):
            create_account()
        
        # Set a payment passcode for 'deposituser'
        accounts = read_accounts()
        accounts['deposituser']['details']['payment_passcode'] = 'password123'
        save_accounts(accounts)

        # Now run the deposit function
        result = deposit('deposituser')
        self.assertTrue(result, "Deposit should succeed.")
        accounts = read_accounts()
        self.assertGreater(accounts['deposituser']['balance'], 0)
        print("Deposit function tested successfully.")

    @patch('builtins.input', side_effect=[
        'withdrawuser', # Username for withdrawal
        'password789', 'password789', # Password for user creation
        'cat', 'dog', # Security questions answers
        'Withdraw User', 'Kenyan', '+254', '799887766', 'withdraw@example.com', 'J333K444L',
        'Savings', 'Artist', 'Freelance', 3, 1, 200.0, '101 Elm St', 1, # Personal details
        '1', # Account type: Current Bank account
        '987654', # OTP
        # Inputs for withdrawal
        '50.0' # Amount to withdraw
    ])
    def test_4_withdraw_function(self, mock_input):
        """Test the withdrawal function."""
        print("\n--- Testing Withdrawal Function ---")
        # Create a user and make them active with some balance
        create_account()
        accounts = read_accounts()
        accounts['withdrawuser']['balance'] = 100.0 # Give them some initial balance
        accounts['withdrawuser']['details']['account_status'] = 'Active' # Ensure active
        save_accounts(accounts)

        result = withdraw('withdrawuser')
        self.assertTrue(result, "Withdrawal should succeed.")
        accounts = read_accounts()
        self.assertEqual(accounts['withdrawuser']['balance'], 50.0)
        print("Withdrawal function tested successfully.")

    def test_5_currency_converter(self):
        """Test the currency_converter function directly."""
        print("\n--- Testing Currency Converter ---")
        # Test USD to KES
        converted_to_kes = currency_converter(10, "USD", "KES")
        self.assertAlmostEqual(converted_to_kes, 10 * USD_TO_KES_RATE)
        print(f"10 USD to KES: {converted_to_kes}")

        # Test KES to USD
        converted_to_usd = currency_converter(1350, "KES", "USD")
        self.assertAlmostEqual(converted_to_usd, 1350 / USD_TO_KES_RATE)
        print(f"1350 KES to USD: {converted_to_usd}")

        # Test same currency
        same_currency = currency_converter(50, "KES", "KES")
        self.assertEqual(same_currency, 50)
        print(f"50 KES to KES: {same_currency}")

        # Test unsupported currency
        unsupported = currency_converter(10, "EUR", "KES")
        self.assertIsNone(unsupported)
        print("Currency converter tested successfully for various scenarios.")

    @patch('builtins.input', side_effect=[
        'txnhistoryuser', 'txnpwd', 'txnpwd', # Username, password
        'dog', 'cat', # Security questions answers
        'Txn History User', 'Kenyan', '+254', '711000111', 'txn@example.com', 'M555N666O',
        'Savings', 'Manager', 'Salary', 4, 2, 1500.0, '222 River Rd', 1, # Personal details
        '1', # Account type: Current Bank account
        '123456' # OTP
    ])
    def test_6_view_transaction_history(self, mock_input):
        """Test viewing transaction history."""
        print("\n--- Testing View Transaction History ---")
        # Create a user and perform some transactions
        create_account()
        accounts = read_accounts()
        accounts['txnhistoryuser']['balance'] = 500.0 # Initial balance
        accounts['txnhistoryuser']['details']['account_status'] = 'Active'
        save_accounts(accounts)

        # Manually add some transactions for this user
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(TRANSACTIONS_FILE, 'a') as f:
            f.write(f"{timestamp},txnhistoryuser,deposit,100.0,Initial deposit\n")
            f.write(f"{timestamp},txnhistoryuser,withdrawal,-50.0,Cash withdrawal\n")
            f.write(f"{timestamp},anotheruser,deposit,200.0,Deposit for other user\n") # Should not appear

        # Capture print output
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            view_transaction_history('txnhistoryuser')
            output = fake_stdout.getvalue()

        self.assertIn("deposit", output)
        self.assertIn("withdrawal", output)
        self.assertNotIn("anotheruser", output)
        print("View transaction history tested successfully.")


if __name__ == '__main__':
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Optional: Run the main banking app after tests
    # print("\n--- Running the main banking application ---")
    # from banking_application import run_banking_app
    # run_banking_app()
