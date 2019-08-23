interface OAuthRequest {
    response_type: 'code' | 'token';
    client_id: string;
    redirect_uri: string;
    scope: string | undefined;
    state: string | undefined;
}
interface OAuthResponse {
    code: string | undefined;
    token: string | undefined;
    state: string | undefined;
}
export { OAuthRequest, OAuthResponse };
