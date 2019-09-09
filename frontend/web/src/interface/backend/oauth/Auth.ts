// logout= '/api/user/login',
import JsonResponse from '@/interface/JsonResponse';
interface OAuthLoginRequest {
    token: string;
    appname: string;
    title: string;
}
interface OAuthLoginResponse extends JsonResponse {
    data: string;
    shortcut: 'ok' | 'pwe' | 'une'  | 'afe';
}
export { OAuthLoginRequest , OAuthLoginResponse };
