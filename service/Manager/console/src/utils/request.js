import Vue from 'vue'
import axios from 'axios'
import qs from 'qs'
import router from '@/router'
import { isArray } from '@/utils/validate'

/**
 * @author https://vue-admin-beautiful.com （不想保留author可删除）
 * @description 处理code异常
 * @param {*} code
 * @param {*} msg
 */
const handleCode = (code, msg) => {
  console.log(msg || `后端接口${code}异常`, 'error')
}



const instance = axios.create({
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
  },
  baseURL:"http://127.0.0.1:7796"
})

instance.interceptors.request.use(
  (config) => {
    if (config.data && config.headers['Content-Type'] === 'application/x-www-form-urlencoded;charset=UTF-8')
      config.data = qs.stringify(config.data)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  (response) => {
    const { data, config } = response
    const { code, message } = data
    let msg = message.split(",")[0] + "[" + code + "]"
    // 是否操作正常
    if (code==0) {
      return data
    } else {
      handleCode(code, msg)
      return Promise.reject(
        `请求异常拦截:${JSON.stringify({
          url: config.url,
          code,
          message: msg,
        })}` || 'Error'
      )
    }
  },
  (error) => {
    const { response, message } = error
    if (error.response && error.response.data) {
      const { status, data } = response
      handleCode(status, data || message)
      return Promise.reject(error)
    } else {
      let { message } = error
      if (message === 'Network Error') {
        message = '后端接口连接异常'
      }
      if (message.includes('timeout')) {
        message = '后端接口请求超时'
      }
      if (message.includes('Request failed with status code')) {
        const code = message.substr(message.length - 3)
        message = `后端接口${code}异常`
      }
      console.log(message || `后端接口未知异常`, 'error')
      return Promise.reject(error)
    }
  }
)

export default instance
