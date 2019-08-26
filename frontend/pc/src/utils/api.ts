const env = process.env ? process.env.NODE_ENV : 'production';
const host = process.env.DEV_HOST || 'localhost';
const devPort = process.env.DEV_PORT || '8000';
const devUrl = `http://${host}:${devPort}`;
const serverUrl = 'http://user.jh.zjut.cn';


enum apiMap {
    authUser = '/api/user/login',
    logout= '/api/user/logout',

    oauth = '/api/oauth/getcode',

    actUser = '/user/activation',
    listUserApp = '/user/app/list',
    deleteUserApp = '/user/app/del',
    getUserInfo = '/user/info',

    authApp = '/api/oauth/checkper',
    alterApp = '/api/oauth/changeapp',
    moveApp = '/api/oauth/move',
 }

/**
 * get API url by API name
 * @return {string}
 */
function API(name: apiMap): string {
    const apiPath = name;
    if (apiPath === undefined) {
        throw new Error('Cannot find a mock API path.');
    }
    const prefix = env === 'development' ? `${devUrl}` : serverUrl;
    const url = `${prefix}${apiPath}`;
    return url;
}

export {apiMap, API };
