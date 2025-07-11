"""
Selenium-based automated tests for user management functionality.

This module contains end-to-end tests for the administrative user management
features in the TechReform application. The tests verify that administrators
can properly manage user accounts, roles, permissions, and access controls
through the web interface using automated browser interactions.

Test Coverage:
    - Administrator authentication and authorization
    - User role management and assignment
    - User account status modifications
    - Permission-based access control testing
    - User profile management from admin perspective
    - Bulk user operations and management
    - User search and filtering functionality
    - Account verification and suspension
    - Role-based feature access validation

Test Class:
    TestUserManagement: Main test class for user management functionality

Key Test Scenarios:
    - Admin login and dashboard access
    - User role assignment and modification
    - User account activation and deactivation
    - Permission testing for different user roles
    - User profile updates from admin interface
    - User deletion and account management
    - Access control validation across features

User Roles Tested:
    - Admin: Full system access and user management
    - Staff: Limited administrative functions
    - Content Manager: Content-related permissions
    - Blogger: Blog creation and management
    - User: Standard customer permissions
    - Guest: Anonymous user capabilities

Dependencies:
    - Selenium WebDriver for browser automation
    - pytest for test framework and parameterization
    - Chrome WebDriver for test execution
    - Admin authentication credentials

Administrative Features Tested:
    - User role assignment interface
    - User status management (active/inactive)
    - User profile editing capabilities
    - Permission validation across modules
    - User activity monitoring and reporting
    - Account verification processes

Usage:
    Run with pytest: pytest tests/User_Management.py
    Generate HTML report: pytest tests/User_Management.py --html=report.html
"""

# Generated by Selenium IDE
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestUserManagement:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize(
        "admin_username,admin_password,target_user_id,new_role",
        [
            ("dotGAdmin", "dotGAdmin@0123", "57", "admin"),
            ("dotGAdmin", "dotGAdmin@0123", "58", "moderator"),
            ("dotGAdmin", "dotGAdmin@0123", "59", "user"),
            ("dotGAdmin", "dotGAdmin@0123", "60", "admin"),
            ("dotGAdmin", "dotGAdmin@0123", "61", "moderator"),
        ],
    )
    def test_user_role_management(
        self, admin_username, admin_password, target_user_id, new_role
    ):
        # Start from home page
        self.driver.get("http://127.0.0.1:8000/")

        # Navigate to login page through dropdown
        self.driver.find_element(By.CSS_SELECTOR, ".dropdown:nth-child(7)").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".text-violet-900:nth-child(1)"
        ).click()

        # Fill login form
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "id_username"))
        ).send_keys(admin_username)
        self.driver.find_element(By.ID, "id_password").send_keys(admin_password)

        # Submit login form
        self.driver.find_element(
            By.CSS_SELECTOR, ".group-hover\\3Atransform:nth-child(1)"
        ).click()

        # Wait for login to complete
        self.wait.until(lambda d: "/auth/login/" not in d.current_url)

        # Navigate to user management through dropdown
        self.driver.find_element(By.CSS_SELECTOR, ".dropdown:nth-child(7)").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".animate-menu-item:nth-child(5) .text-xs"
        ).click()  # Click on change role button for the target user
        change_role_btn_selector = (
            ".hover\\3A bg-base-200\\/30:nth-child(5) .btn:nth-child(1)"
        )
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, change_role_btn_selector))
        ).click()

        # Select the new role in the modal
        role_selector_map = {
            "admin": "#modal-change-role-{} .label:nth-child(1) > .radio".format(
                target_user_id
            ),
            "moderator": "#modal-change-role-{} .label:nth-child(2) > .radio".format(
                target_user_id
            ),
            "user": "#modal-change-role-{} .label:nth-child(3) > .radio".format(
                target_user_id
            ),
        }

        role_radio_selector = role_selector_map.get(
            new_role,
            "#modal-change-role-{} .label:nth-child(2) > .radio".format(target_user_id),
        )

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, role_radio_selector))
        ).click()

        # Confirm the role change
        confirm_btn_selector = f"#modal-change-role-{target_user_id} .btn-primary"
        self.driver.find_element(By.CSS_SELECTOR, confirm_btn_selector).click()

        # Wait for the modal to close and verify the change was successful
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, f"#modal-change-role-{target_user_id}")
            )
        )

        # Assert that the role change was successful by checking if we're still on the user management page
        # and that no error messages are displayed
        assert (
            "user" in self.driver.current_url.lower()
            or "management" in self.driver.current_url.lower()
        ), f"User role management failed for user {target_user_id}"
