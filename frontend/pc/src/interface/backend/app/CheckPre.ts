// // path('api/oauth/checkper', oauth.checkper, name='oauth.checkper'),
import JsonResponse from '@/interface/JsonResponse';
// interface Request {
//     studentId: string;
//     password: string;
// }
interface CheckPreResponse extends JsonResponse {
    data: {
        name: string,
    };
    shortcut: 'ok' | 'pwe' | 'une'  | 'afe';
}
export {CheckPreResponse};
