// logout= '/api/user/login',
import JsonResponse from '@/interface/JsonResponse';
interface LogoutRequest {
    token: string;
}
interface LogoutResponse extends JsonResponse {
    shortcut: 'ok'  | 'afe'  ;
    msg: string;
}
export { LogoutRequest, LogoutResponse };
