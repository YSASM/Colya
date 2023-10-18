<template>
  <div>
      <el-card shadow="always" :body-style="{ padding: '20px' }">
          <div slot="header">
              <span>日志</span>
          </div>
          <div class="log">
              <el-card class="log-card" shadow="always" :body-style="{ padding: '10px' }" v-for="log,i in logs" :key="i">
                  {{log}}
              </el-card>
          </div>
          <div class="cmd">
              <el-input v-model="cmdInput" class="input" placeholder="输入cmd指令/help获取帮助" @keyup.enter.native="sendCmd()"></el-input>
              <el-button type="success" class="btn" @click="sendCmd()">发送</el-button>
          </div>
      </el-card>
      
  </div>   
  </template>
  <script>
  import api from '@/api/index.js'
  export default{
      data(){
          return {
              logs:[],
              cmdInput:""
          }
      },
      mounted(){
          this.getData()
          setInterval(() => {
              this.getData()
          }, 4000);
      },
      methods:{
          getData(){
              api.getData().then(res=>{
                  this.logs = res.data.consoleLog
                  this.$forceUpdate()
              })
          },
          sendCmd(){
              api.sendCmd({
                  cmd:this.cmdInput
              }).then(res=>{
                  this.cmdInput = ""
              })
          }
      }
  }
  </script>
  <style lang="scss" scoped>
  .log{
      padding: 10px;
      height: 650px;
      overflow:auto;
      border: 1px solid rgb(235, 235, 235);
      .log-card{
          white-space: break-spaces;
          margin-top: 10px;
          text-align: start;
      }
  }
  .cmd{
      display: flex;
      flex-direction: row;
      padding-top: 20px;
      justify-content: space-between;
      .input{
          width: 95%;
      }
  }
  </style>