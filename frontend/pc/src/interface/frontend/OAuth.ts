interface OAuthRequest {
    response_type: 'code' | 'token';
    client_id: string;
    redirect_uri: string;
    scope: string | undefined;
    state: string | undefined;
}
interface OAuthCodeResponse {
    code: string ;
    state: string ;
}
interface OAuthTokenResponse {
    token: string ;
    state: string ;
}
interface OAuthError {
    error: string ;
    error_description: string | undefined;
    error_uri: string | undefined;
    state: string ;
}
export { OAuthRequest, OAuthCodeResponse, OAuthTokenResponse, OAuthError };
