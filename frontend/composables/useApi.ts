import type { UseFetchOptions } from "nuxt/app";

/**
 * API 请求封装
 * 自动带上 baseURL，统一错误处理
 */
export function useApi<T>(url: string, options: UseFetchOptions<T> = {}) {
  const config = useRuntimeConfig();

  return useFetch(url, {
    baseURL: config.public.apiBase,
    ...options,
    onResponseError({ response }) {
      console.error(`API Error [${response.status}]:`, response._data);
    },
  });
}
