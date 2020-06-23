const awsmobile = {
    "aws_project_region": "us-east-1",
    "aws_cognito_identity_pool_id": "us-east-1:b3c001ae-1fa0-485b-9ad8-d5cd80c4c5a4",
    "aws_cognito_region": "us-east-1",
    "aws_user_pools_id": "us-east-1_IE9ZciRMz",
    "aws_user_pools_web_client_id": "6qk9ep6qt2g349v2gg7uff1h65",
    "oauth": {
        "domain": "con-pca-develop.auth.us-east-1.amazoncognito.com",
        "scope": [
            "phone",
            "email",
            "openid",
            "profile",
            "aws.cognito.signin.user.admin"
        ],
        "redirectSignIn": "http://iaadevelop.inl.gov:4200/",
        "redirectSignOut": "http://iaadevelop.inl.gov:4200/",
        "responseType": "code"
    },
    "federationTarget": "COGNITO_USER_POOLS"
};

export default awsmobile;