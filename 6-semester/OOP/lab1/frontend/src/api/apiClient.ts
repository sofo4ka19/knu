import axios from 'axios'

const BASE_URL = 'http://localhost:8080/api'

export const publicApi = axios.create({ baseURL: BASE_URL })

export const createAuthApi = (getToken: () => Promise<string>) => {
    const api = axios.create({ baseURL: BASE_URL })

    api.interceptors.request.use(async (config) => {
        const token = await getToken()
        config.headers.Authorization = `Bearer ${token}`
        return config
    })

    api.interceptors.response.use(
        res => res,
        err => {
            const msg = err.response?.data?.error || 'Помилка сервера'
            return Promise.reject(new Error(msg))
        }
    )

    return api
}