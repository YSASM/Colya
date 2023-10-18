const express = require('express')
const app = express()
const compression = require('compression')
const { default: axios } = require('axios')
 
app.use(compression()) // 一定要把这一行写在 静态资源托管之前
app.use(express.static(__dirname+'/dist'))
axios.get("http://127.0.0.1:7796/test")
  .then(response => {
    app.listen(8080,()=> {
        console.log('server running at http://127.0.0.1:8080')
    })
  })
  .catch(error => {
    // 请求失败处理
    console.error("服务端未开启");
  });
