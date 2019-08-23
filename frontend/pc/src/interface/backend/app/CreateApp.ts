// logout= '/api/user/login',
import JsonResponse from '@/interface/JsonResponse';
interface CreateAppRequest {
    token: string;
    appname: string;
    title: string;
    description: string;
    tags: string;
    level: string;
}
interface CreateAppResponse extends JsonResponse {
    data: {
        name: string,
        owner: string,
        level: string,
        create_time: string,
        description: string,
        tags: string,
        state: string,
    };
}
export { CreateAppRequest, CreateAppResponse };
