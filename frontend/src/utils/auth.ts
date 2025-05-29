// Auth utility functions
export const setToken = (token: string): void => {
  localStorage.setItem('token', token);
};

export const getToken = (): string | null => {
  return localStorage.getItem('token');
};

export const removeToken = (): void => {
  localStorage.removeItem('token');
};

export const setAccountId = (accountId: string): void => {
  localStorage.setItem('account_id', accountId);
};

export const getAccountId = (): string | null => {
  return localStorage.getItem('account_id');
};

export const removeAccountId = (): void => {
  localStorage.removeItem('account_id');
};

export const isAuthenticated = (): boolean => {
  return !!getToken();
};

export const logout = (): void => {
  removeToken();
  removeAccountId();
}; 