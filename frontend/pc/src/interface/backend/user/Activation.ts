// ,
import JsonResponse from '@/interface/JsonResponse';
interface ActivationRequest {
    id: string;
    idCard: string;
    email: string;
    password: string;
}
interface ActivationResponse extends JsonResponse {
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
    shortcut: 'ok' | 'pe' | 'une'  | 'ae';
}
export {ActivationRequest , ActivationResponse };
