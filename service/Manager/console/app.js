const express = require('express')
const app = express()
const compression = require('compression')
 
app.use(compression()) // 一定要把这一行写在 静态资源托管之前
app.use(express.static(__dirname+'/dist'))
 
app.listen(8080,()=> {
  console.log('server running at http://127.0.0.1:8080')
})