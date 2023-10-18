import { requests } from '@/api/default'

export default {
  async getData(params) {
    return requests({
      url: '/data',
      method: 'get',
    })(params)
  },
  async sendCmd(data) {
    return requests({
      url: '/cmd',
      method: 'post',
    })(data)
  }
}

