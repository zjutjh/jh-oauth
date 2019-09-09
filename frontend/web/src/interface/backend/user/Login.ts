// logout= '/api/user/login',
import JsonResponse from '@/interface/JsonResponse';
interface LoginRequest {
    name: string;
    password: string;
    device_type: string;
    token?: string;
}
interface LoginResponse extends JsonResponse {
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
    shortcut: 'ok' | 'pwe' | 'une' | 'afe';
    msg: string;
}
export { LoginRequest, LoginResponse };
