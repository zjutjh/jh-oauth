export default class {

    public static idCard(val: string): boolean {
         /** 检查二代身份证是否合法 */
        const reg = /^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/;
        /** 检查护照是否合法 */
        const reg1 = /^[a-zA-Z]{5,17}$/;
        const reg2 = /^[a-zA-Z0-9]{5,17}$/;
        /** 港澳通行证验证   */
        const reg3 = /^[HMhm]{1}([0-9]{10}|[0-9]{8})$/;
        /** 台湾通行证验证   */
        const reg4 = /^[0-9]{8}$/;
        const reg5 = /^[0-9]{10}$/;

        if (reg.test(val) === false
            && reg1.test(val) === false
            && reg2.test(val) === false
            && reg3.test(val) === false
            && reg4.test(val) === false
            && reg5.test(val) === false) {
            return false;
        }
        return true;
    }
    public static mobilePhone(val: string): boolean {
        const reg = /^1(3|4|5|6|7|8|9)\d{9}$/;
        if (reg.test(val) === false) {
            return false;
        }
        return true;
    }
    public static jhNum(val: string): boolean {
        const reg = /^[0-9a-zA-Z_]{1,}$/;
        if (reg.test(val) === false) {
            return false;
        }
        return true;
    }
    public static password(val: string): boolean {
        const reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/;
        if (reg.test(val) === false) {
            return false;
        }
        return true;
    }
    public static mail(val: string): boolean {
        const reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/;
        if (reg.test(val) === false) {
            return false;
        }
        return true;
    }
}
