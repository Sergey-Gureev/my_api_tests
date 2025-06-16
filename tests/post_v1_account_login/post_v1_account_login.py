
from hamcrest import assert_that, has_property, equal_to, has_items
from clients.http.dm_api_account.models.user_envelope import UserRole


def test_post_v1_account_login_positive_flow(registered_user, account_helper):
    response = account_helper.user_login(
        login=registered_user.login,
        password=registered_user.password,
        remember_me= True,
        return_model=True)
    print(response)
    assert_that(response, has_property("resource", has_property("login", equal_to(registered_user.login))))
    assert_that(response.resource.roles, has_items(UserRole.GUEST, UserRole.PLAYER))
