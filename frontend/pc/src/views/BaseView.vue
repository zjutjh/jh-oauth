<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { CheckPreResponse } from '../interface/backend/app/CheckPre';
import { Error } from '../utils/error';
import { routerPath } from '../utils/routerPath';
import stringFilter from '../utils/stringFilter';
@Component
export default class BaseView extends Vue {
  public idFilter = stringFilter.jhNum;
  public passFilter = stringFilter.password;
  public idCardFilter = stringFilter.idCard;
  public mailFilter = stringFilter.mail;

  public isError: boolean = false;
  public errorMsg: string = '';
  public isTipClicked: boolean = false;
  public tipMsg: string = '';

  public isWaiting: boolean = false;
  public aboutClick() {
    this.$router.push(routerPath.about);
  }
  public closeDialog() {
    this.isTipClicked = false;
    this.isError = false;
  }
  public tipClick() {
    this.isTipClicked = true;
  }
  public setError(error: string | Error) {
    this.isWaiting = false;
    this.isError = true;
    this.errorMsg = error;
  }
}
</script>