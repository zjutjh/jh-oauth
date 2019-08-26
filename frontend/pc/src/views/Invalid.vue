<template>
  <card class="auth-panel" title="错误">
    <div style="margin:2rem">
      ipsum dolor sit amet consectetur, adipisicing elit.iure provident voluptatem animi, facilis nisi minima atque quo incidunt exercitationem itaque? Voluptates quaerat similique harum ex, veritatis doloribus facilis corporis odio ab mollitia cumque molestias. Beatae doloribus, consequuntur excepturi magnam, molestiae ipsam neque ducimus laboriosam voluptate eveniet ipsa dignissimos molestias veniam distinctio aut? Ut, quaerat illum illo, similique magni ratione vel optio nesciunt harum voluptate perferendis sit quo hic beatae aspernatur quidem molestias? At temporibus officia accusantium nihil quos voluptas vel illum voluptatibus assumenda, id possimus autem adipisci itaque ducimus quia, minima expedita reprehenderit?
    </div>
     <v-button class="Stbotton" text="返回" @click="back"></v-button>
  </card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import VButton from '../components/Button.vue';
import Card from '../components/Card.vue';
@Component({ components: { Card, VButton } })
export default class Invalid extends Vue {
  private back() {
    this.$router.back();
  }
}
</script>
