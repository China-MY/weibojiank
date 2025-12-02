import api from './axios';

export const login = (username, password) => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);
  params.append('grant_type', 'password');
  return api.post('/token', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
};

export const getWeiboList = () => api.get('/weibo/list');

export const getExpiredWeiboList = (days = 3) => api.get(`/weibo/expired?days=${days}`);

export const addWeiboAccount = (uid, screenName, checkInterval = 3600) => 
  api.post('/weibo/add', { uid, screen_name: screenName, check_interval: checkInterval });

export const removeWeiboAccount = (id) => api.delete(`/weibo/remove/${id}`);

export const getSystemConfig = (key) => api.get(`/settings/${key}`);
export const saveSystemConfig = (key, value, description) => api.post('/settings/', { key, value, description });

export const getExpiredReport = (days) => api.get(`/weibo/expired_report${days ? `?days=${days}` : ''}`);

export const checkAccount = (uid) => api.post(`/weibo/check/${uid}`);

export const setBatchInterval = (seconds) => api.post('/weibo/batch_interval', { seconds });
export const testWebhook = () => api.post('/weibo/webhook_test');
export const updateUserCredentials = (current_password, username, password) => api.post('/users/update', { current_password, username, password });
export const getMe = () => api.get('/me');
export const pushSummary = (days) => api.post('/weibo/push_summary', null, { params: { days } });
