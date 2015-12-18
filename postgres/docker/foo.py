from vmauto.pages.myapps import MyAppsPage
import vmauto.client
import mock

@mock.patch("vmauto.client.Session.post")
def test_login(mock_post):

    host = "https://176.16.64.201"
    username = "someuser"
    password = "somepassword"

    post_data = {"username": username, "password": password}

    client = vmauto.client.MobileClient(host, username, password, verify=False)
    client.login()

    mock_post.assert_called_with(
        "{0}/login".format(host),
        headers=None,
        data=post_data,
        verify=False
    )
