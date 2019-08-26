// logout= '/api/user/login',
import JsonResponse from '@/interface/JsonResponse';
interface AutoLoginRequest {
    token: string;
}
interface AutoLoginResponse extends JsonResponse {
    data: {
        access_time: string,
        token: string,
        username: string,
        email: string,
        nickname: string,
        create_time: string,
        user_type: string,
        permission: string,
    };
    shortcut: 'ok' | 'pwe' | 'une' | 'afe' | 'tle';
}
export { AutoLoginRequest, AutoLoginResponse };
